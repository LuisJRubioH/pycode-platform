// store/eloStore.ts
// Zustand store para el sistema ELO de PyCode

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface EloProfile {
  elo_rating: number;
  elo_peak: number;
  rank: string;
  rank_color: string;
  puzzles_attempted: number;
  puzzles_correct: number;
  accuracy: number;
  streak_current: number;
  streak_best: number;
}

interface PuzzleAttemptResult {
  correct: boolean;
  correct_output: string;
  explanation: string;
  user_elo_before: number;
  user_elo_after: number;
  elo_delta_user: number;
  puzzle_elo_before: number;
  puzzle_elo_after: number;
  rank_before: string;
  rank_after: string;
  rank_changed: boolean;
  rank_color: string;
  expected_probability: number;
  win_probability_label: string;
}

interface EloStore {
  profile: EloProfile | null;
  lastResult: PuzzleAttemptResult | null;
  isSubmitting: boolean;

  // Acciones
  fetchProfile: () => Promise<void>;
  submitAttempt: (puzzleId: number, answer: string, timeSeconds?: number) => Promise<PuzzleAttemptResult>;
  clearLastResult: () => void;
}

const API_BASE = "/api";

function authHeaders() {
  const token = localStorage.getItem("access_token");
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

export const useEloStore = create<EloStore>()(
  persist(
    (set, get) => ({
      profile: null,
      lastResult: null,
      isSubmitting: false,

      fetchProfile: async () => {
        try {
          const res = await fetch(`${API_BASE}/elo/profile`, { headers: authHeaders() });
          if (!res.ok) throw new Error("Failed to fetch profile");
          const data: EloProfile = await res.json();
          set({ profile: data });
        } catch (err) {
          console.error("ELO profile fetch error:", err);
        }
      },

      submitAttempt: async (puzzleId, answer, timeSeconds) => {
        set({ isSubmitting: true });
        try {
          const res = await fetch(`${API_BASE}/elo/attempt`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({
              puzzle_id: puzzleId,
              user_answer: answer,
              time_spent_seconds: timeSeconds,
            }),
          });

          if (!res.ok) throw new Error("Failed to submit attempt");

          const result: PuzzleAttemptResult = await res.json();
          set({ lastResult: result });

          // Actualizar el perfil local inmediatamente sin esperar un fetch
          const current = get().profile;
          if (current) {
            set({
              profile: {
                ...current,
                elo_rating: result.user_elo_after,
                elo_peak: Math.max(current.elo_peak, result.user_elo_after),
                rank: result.rank_after,
                rank_color: result.rank_color,
                puzzles_attempted: current.puzzles_attempted + 1,
                puzzles_correct: result.correct
                  ? current.puzzles_correct + 1
                  : current.puzzles_correct,
                streak_current: result.correct
                  ? current.streak_current + 1
                  : 0,
                streak_best: result.correct
                  ? Math.max(current.streak_best, current.streak_current + 1)
                  : current.streak_best,
                accuracy: parseFloat(
                  (((result.correct ? current.puzzles_correct + 1 : current.puzzles_correct) /
                    (current.puzzles_attempted + 1)) * 100).toFixed(1)
                ),
              },
            });
          }

          return result;
        } finally {
          set({ isSubmitting: false });
        }
      },

      clearLastResult: () => set({ lastResult: null }),
    }),
    {
      name: "pycode-elo",
      // Solo persistir el perfil localmente como caché —
      // la fuente de verdad es siempre el backend
      partialize: (state) => ({ profile: state.profile }),
    }
  )
);

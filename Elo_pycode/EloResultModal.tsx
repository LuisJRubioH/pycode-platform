// EloResultModal.tsx
// Modal que aparece después de cada intento de puzzle con el resultado ELO

import { useEffect, useState } from "react";

interface EloResultModalProps {
  result: {
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
  };
  onClose: () => void;
  onNextPuzzle: () => void;
}

export default function EloResultModal({ result, onClose, onNextPuzzle }: EloResultModalProps) {
  const [animating, setAnimating] = useState(false);
  const [displayElo, setDisplayElo] = useState(result.user_elo_before);

  // Animar el contador de ELO
  useEffect(() => {
    setAnimating(true);
    const target = result.user_elo_after;
    const start = result.user_elo_before;
    const diff = target - start;
    const steps = 30;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      setDisplayElo(Math.round(start + (diff * step) / steps));
      if (step >= steps) {
        clearInterval(timer);
        setDisplayElo(target);
      }
    }, 20);

    return () => clearInterval(timer);
  }, [result]);

  const isPositive = result.elo_delta_user > 0;
  const color = result.rank_color;

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      background: "rgba(0,0,0,0.5)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000,
      padding: 20,
    }}>
      <div style={{
        background: "var(--color-background-primary)",
        borderRadius: 20,
        padding: "32px 36px",
        maxWidth: 480,
        width: "100%",
        border: `2px solid ${result.correct ? "#10B981" : "#EF4444"}22`,
        boxShadow: `0 0 0 1px ${result.correct ? "#10B981" : "#EF4444"}33`,
      }}>

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: 24 }}>
          <div style={{
            fontSize: 48,
            marginBottom: 8,
          }}>
            {result.correct ? "✓" : "✗"}
          </div>
          <div style={{
            fontSize: 22,
            fontWeight: 700,
            color: result.correct ? "#10B981" : "#EF4444",
          }}>
            {result.correct ? "¡Correcto!" : "Incorrecto"}
          </div>
        </div>

        {/* ELO Change */}
        <div style={{
          background: "var(--color-background-secondary)",
          borderRadius: 14,
          padding: "20px 24px",
          marginBottom: 20,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}>
          <div>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 4 }}>
              Tu ELO
            </div>
            <div style={{
              fontSize: 40,
              fontWeight: 700,
              fontFamily: "monospace",
              color,
            }}>
              {displayElo.toLocaleString()}
            </div>
            <div style={{
              fontSize: 16,
              fontWeight: 600,
              color: isPositive ? "#10B981" : "#EF4444",
              marginTop: 4,
            }}>
              {isPositive ? "+" : ""}{result.elo_delta_user} pts
            </div>
          </div>

          {/* Rank */}
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 6 }}>
              Rango
            </div>
            <div style={{
              background: color + "22",
              border: `1px solid ${color}44`,
              borderRadius: 8,
              padding: "6px 12px",
              fontSize: 13,
              fontWeight: 600,
              color,
            }}>
              {result.rank_after}
            </div>
            {result.rank_changed && (
              <div style={{
                fontSize: 11,
                color: "#10B981",
                marginTop: 6,
                fontWeight: 600,
              }}>
                ↑ Nuevo rango!
              </div>
            )}
          </div>
        </div>

        {/* Probabilidad esperada */}
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 12,
          color: "var(--color-text-secondary)",
          padding: "0 4px",
          marginBottom: 16,
        }}>
          <span>Dificultad para ti: <strong style={{ color: "var(--color-text-primary)" }}>
            {result.win_probability_label}
          </strong></span>
          <span>{Math.round(result.expected_probability * 100)}% prob. esperada</span>
        </div>

        {/* Solución correcta (si falló) */}
        {!result.correct && (
          <div style={{
            background: "#FEF2F2",
            border: "1px solid #FECACA",
            borderRadius: 10,
            padding: "12px 16px",
            marginBottom: 16,
          }}>
            <div style={{ fontSize: 11, color: "#991B1B", fontWeight: 600, marginBottom: 6 }}>
              Solución correcta:
            </div>
            <code style={{ fontSize: 14, color: "#7F1D1D", fontFamily: "monospace" }}>
              {result.correct_output}
            </code>
          </div>
        )}

        {/* Explicación */}
        <div style={{
          background: "var(--color-background-secondary)",
          borderRadius: 10,
          padding: "12px 16px",
          fontSize: 13,
          color: "var(--color-text-secondary)",
          lineHeight: 1.6,
          marginBottom: 24,
        }}>
          {result.explanation}
        </div>

        {/* Tabla ELO de referencia */}
        <div style={{
          fontSize: 11,
          color: "var(--color-text-tertiary)",
          textAlign: "center",
          marginBottom: 20,
        }}>
          ELO del puzzle: {result.puzzle_elo_before} → {result.puzzle_elo_after}
        </div>

        {/* Botones */}
        <div style={{ display: "flex", gap: 12 }}>
          <button
            onClick={onClose}
            style={{
              flex: 1,
              padding: "12px",
              background: "transparent",
              border: "0.5px solid var(--color-border-secondary)",
              borderRadius: 10,
              cursor: "pointer",
              fontSize: 14,
              color: "var(--color-text-secondary)",
            }}
          >
            Ver editor
          </button>
          <button
            onClick={onNextPuzzle}
            style={{
              flex: 2,
              padding: "12px",
              background: color,
              border: "none",
              borderRadius: 10,
              cursor: "pointer",
              fontSize: 14,
              fontWeight: 600,
              color: "#fff",
            }}
          >
            Siguiente puzzle →
          </button>
        </div>
      </div>
    </div>
  );
}

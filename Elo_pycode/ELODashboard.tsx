// ELODashboard.tsx
// Dashboard de progreso ELO para PyCode Platform
// Inspirado en Coffee Break Python (Christian Mayer / Finxter)

import { useState, useEffect, useCallback } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine, Area, AreaChart
} from "recharts";

// ─── Types ────────────────────────────────────────────────────────────────────

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

interface EloHistoryPoint {
  elo_value: number;
  delta: number;
  correct: boolean;
  rank_label: string;
  puzzle_title: string;
  category: string;
  created_at: string;
}

interface RankRow {
  elo_min: number;
  elo_max: number | null;
  rank: string;
  color: string;
  is_current: boolean;
}

const RANK_THRESHOLDS: RankRow[] = [
  { elo_min: 2500, elo_max: null, rank: "World Class",             color: "#F97316", is_current: false },
  { elo_min: 2400, elo_max: 2500, rank: "Grandmaster",             color: "#EC4899", is_current: false },
  { elo_min: 2300, elo_max: 2400, rank: "International Master",    color: "#EC4899", is_current: false },
  { elo_min: 2200, elo_max: 2300, rank: "Master",                  color: "#8B5CF6", is_current: false },
  { elo_min: 2100, elo_max: 2200, rank: "National Master",         color: "#8B5CF6", is_current: false },
  { elo_min: 2000, elo_max: 2100, rank: "Master Candidate",        color: "#EF4444", is_current: false },
  { elo_min: 1900, elo_max: 2000, rank: "Authority",               color: "#EF4444", is_current: false },
  { elo_min: 1800, elo_max: 1900, rank: "Professional",            color: "#F59E0B", is_current: false },
  { elo_min: 1700, elo_max: 1800, rank: "Expert",                  color: "#F59E0B", is_current: false },
  { elo_min: 1600, elo_max: 1700, rank: "Experienced Intermediate",color: "#10B981", is_current: false },
  { elo_min: 1500, elo_max: 1600, rank: "Intermediate",            color: "#10B981", is_current: false },
  { elo_min: 1400, elo_max: 1500, rank: "Experienced Learner",     color: "#06B6D4", is_current: false },
  { elo_min: 1300, elo_max: 1400, rank: "Learner",                 color: "#06B6D4", is_current: false },
  { elo_min: 1200, elo_max: 1300, rank: "Scholar",                 color: "#3B82F6", is_current: false },
  { elo_min: 1100, elo_max: 1200, rank: "Autodidact",              color: "#3B82F6", is_current: false },
  { elo_min: 1000, elo_max: 1100, rank: "Beginner",                color: "#6B7280", is_current: false },
  { elo_min: 0,    elo_max: 1000, rank: "Basic Knowledge",         color: "#6B7280", is_current: false },
];

// ─── Hooks ────────────────────────────────────────────────────────────────────

function useEloData() {
  const [profile, setProfile] = useState<EloProfile | null>(null);
  const [history, setHistory] = useState<EloHistoryPoint[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const token = localStorage.getItem("access_token");
      const headers = { Authorization: `Bearer ${token}` };

      const [profileRes, historyRes] = await Promise.all([
        fetch("/api/elo/profile", { headers }),
        fetch("/api/elo/history?limit=100", { headers }),
      ]);

      const profileData = await profileRes.json();
      const historyData = await historyRes.json();

      setProfile(profileData);
      setHistory(historyData.history || []);
    } catch (err) {
      console.error("Error fetching ELO data:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  return { profile, history, loading, refetch: fetchData };
}

// ─── Sub-componentes ──────────────────────────────────────────────────────────

function EloMeter({ elo, rank, color }: { elo: number; rank: string; color: string }) {
  const maxElo = 2500;
  const pct = Math.min((elo / maxElo) * 100, 100);

  return (
    <div style={{
      background: "var(--color-background-primary)",
      border: "0.5px solid var(--color-border-tertiary)",
      borderRadius: 16,
      padding: "24px 28px",
      display: "flex",
      flexDirection: "column",
      gap: 16,
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div style={{ fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 6 }}>
            Tu rating ELO
          </div>
          <div style={{ fontSize: 52, fontWeight: 700, color, lineHeight: 1, fontFamily: "monospace" }}>
            {elo.toLocaleString()}
          </div>
        </div>
        <div style={{
          background: color + "22",
          border: `1px solid ${color}55`,
          borderRadius: 10,
          padding: "8px 14px",
          fontSize: 13,
          fontWeight: 600,
          color,
          textAlign: "center",
          maxWidth: 140,
        }}>
          {rank}
        </div>
      </div>

      {/* Barra de progreso */}
      <div>
        <div style={{
          height: 8,
          borderRadius: 4,
          background: "var(--color-background-secondary)",
          overflow: "hidden",
        }}>
          <div style={{
            height: "100%",
            width: `${pct}%`,
            background: color,
            borderRadius: 4,
            transition: "width 1s ease",
          }} />
        </div>
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 11,
          color: "var(--color-text-tertiary)",
          marginTop: 4,
        }}>
          <span>0</span>
          <span>2500 — World Class</span>
        </div>
      </div>
    </div>
  );
}

function StatCard({ label, value, sub }: { label: string; value: string | number; sub?: string }) {
  return (
    <div style={{
      background: "var(--color-background-secondary)",
      borderRadius: 12,
      padding: "14px 16px",
    }}>
      <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 24, fontWeight: 600, color: "var(--color-text-primary)" }}>{value}</div>
      {sub && <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginTop: 2 }}>{sub}</div>}
    </div>
  );
}

function EloChart({ history }: { history: EloHistoryPoint[] }) {
  if (history.length === 0) {
    return (
      <div style={{
        background: "var(--color-background-primary)",
        border: "0.5px solid var(--color-border-tertiary)",
        borderRadius: 16,
        padding: 24,
        textAlign: "center",
        color: "var(--color-text-secondary)",
        fontSize: 14,
      }}>
        Resuelve tu primer puzzle para ver tu curva de progreso ELO
      </div>
    );
  }

  const chartData = history.map((p, i) => ({
    puzzle: i + 1,
    elo: p.elo_value,
    delta: p.delta,
    correct: p.correct,
    title: p.puzzle_title,
    category: p.category,
  }));

  const minElo = Math.min(...chartData.map(d => d.elo)) - 50;
  const maxElo = Math.max(...chartData.map(d => d.elo)) + 50;

  const CustomDot = (props: any) => {
    const { cx, cy, payload } = props;
    return (
      <circle
        cx={cx} cy={cy} r={4}
        fill={payload.correct ? "#10B981" : "#EF4444"}
        stroke="var(--color-background-primary)"
        strokeWidth={2}
      />
    );
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload?.length) return null;
    const d = payload[0].payload;
    return (
      <div style={{
        background: "var(--color-background-primary)",
        border: "0.5px solid var(--color-border-secondary)",
        borderRadius: 10,
        padding: "10px 14px",
        fontSize: 12,
      }}>
        <div style={{ fontWeight: 600, marginBottom: 4, color: "var(--color-text-primary)" }}>
          {d.title}
        </div>
        <div style={{ color: "var(--color-text-secondary)" }}>ELO: {d.elo}</div>
        <div style={{ color: d.correct ? "#10B981" : "#EF4444", fontWeight: 500 }}>
          {d.correct ? `+${d.delta}` : d.delta} pts
        </div>
        <div style={{
          marginTop: 4,
          fontSize: 11,
          background: d.category === "numpy" ? "#E1F5EE" : d.category === "pandas" ? "#E6F1FB" : "#EEEDFE",
          color: d.category === "numpy" ? "#0F6E56" : d.category === "pandas" ? "#185FA5" : "#534AB7",
          padding: "2px 6px",
          borderRadius: 4,
          display: "inline-block",
        }}>
          {d.category}
        </div>
      </div>
    );
  };

  return (
    <div style={{
      background: "var(--color-background-primary)",
      border: "0.5px solid var(--color-border-tertiary)",
      borderRadius: 16,
      padding: "20px 24px",
    }}>
      <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 16, color: "var(--color-text-primary)" }}>
        Curva de progreso ELO
      </div>
      <div style={{ height: 220 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
            <defs>
              <linearGradient id="eloGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366F1" stopOpacity={0.15} />
                <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-tertiary)" />
            <XAxis
              dataKey="puzzle"
              tick={{ fontSize: 11, fill: "var(--color-text-tertiary)" }}
              label={{ value: "Puzzles resueltos", position: "insideBottom", offset: -2, fontSize: 11, fill: "var(--color-text-secondary)" }}
            />
            <YAxis
              domain={[minElo, maxElo]}
              tick={{ fontSize: 11, fill: "var(--color-text-tertiary)" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="elo"
              stroke="#6366F1"
              strokeWidth={2}
              fill="url(#eloGrad)"
              dot={<CustomDot />}
              activeDot={{ r: 6 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div style={{ display: "flex", gap: 16, marginTop: 12, fontSize: 12, color: "var(--color-text-secondary)" }}>
        <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#10B981", display: "inline-block" }} />
          Correcto
        </span>
        <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#EF4444", display: "inline-block" }} />
          Incorrecto
        </span>
      </div>
    </div>
  );
}

function RankTable({ userElo }: { userElo: number }) {
  const [expanded, setExpanded] = useState(false);
  const ranks = RANK_THRESHOLDS.map(r => ({
    ...r,
    is_current: userElo >= r.elo_min && (r.elo_max === null || userElo < r.elo_max),
  }));

  const visible = expanded ? ranks : ranks.filter((_, i) => {
    const currentIdx = ranks.findIndex(r => r.is_current);
    return Math.abs(i - currentIdx) <= 2;
  });

  return (
    <div style={{
      background: "var(--color-background-primary)",
      border: "0.5px solid var(--color-border-tertiary)",
      borderRadius: 16,
      overflow: "hidden",
    }}>
      <div style={{ padding: "16px 20px", borderBottom: "0.5px solid var(--color-border-tertiary)" }}>
        <div style={{ fontSize: 14, fontWeight: 500, color: "var(--color-text-primary)" }}>
          Tabla de rangos ELO
        </div>
        <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginTop: 2 }}>
          Según Coffee Break Python (Finxter)
        </div>
      </div>

      <div>
        {visible.map((row) => (
          <div key={row.rank} style={{
            display: "grid",
            gridTemplateColumns: "100px 1fr",
            padding: "10px 20px",
            borderBottom: "0.5px solid var(--color-border-tertiary)",
            background: row.is_current ? row.color + "12" : "transparent",
            borderLeft: row.is_current ? `3px solid ${row.color}` : "3px solid transparent",
            transition: "background 0.2s",
          }}>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)", fontFamily: "monospace" }}>
              {row.elo_max ? `${row.elo_min}–${row.elo_max}` : `≥${row.elo_min}`}
            </div>
            <div style={{
              fontSize: 13,
              fontWeight: row.is_current ? 600 : 400,
              color: row.is_current ? row.color : "var(--color-text-primary)",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}>
              {row.rank}
              {row.is_current && (
                <span style={{
                  fontSize: 10,
                  background: row.color,
                  color: "#fff",
                  padding: "2px 6px",
                  borderRadius: 4,
                  fontWeight: 600,
                }}>
                  TÚ
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={() => setExpanded(!expanded)}
        style={{
          width: "100%",
          padding: "12px",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          fontSize: 12,
          color: "var(--color-text-secondary)",
          borderTop: "0.5px solid var(--color-border-tertiary)",
        }}
      >
        {expanded ? "Mostrar menos ↑" : "Ver tabla completa ↓"}
      </button>
    </div>
  );
}

function RecentActivity({ history }: { history: EloHistoryPoint[] }) {
  const recent = [...history].reverse().slice(0, 8);
  if (recent.length === 0) return null;

  return (
    <div style={{
      background: "var(--color-background-primary)",
      border: "0.5px solid var(--color-border-tertiary)",
      borderRadius: 16,
      overflow: "hidden",
    }}>
      <div style={{ padding: "16px 20px", borderBottom: "0.5px solid var(--color-border-tertiary)" }}>
        <div style={{ fontSize: 14, fontWeight: 500, color: "var(--color-text-primary)" }}>
          Actividad reciente
        </div>
      </div>
      {recent.map((p, i) => (
        <div key={i} style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px 20px",
          borderBottom: i < recent.length - 1 ? "0.5px solid var(--color-border-tertiary)" : "none",
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{
              width: 6, height: 6, borderRadius: "50%",
              background: p.correct ? "#10B981" : "#EF4444",
              flexShrink: 0,
            }} />
            <div>
              <div style={{ fontSize: 13, color: "var(--color-text-primary)" }}>{p.puzzle_title}</div>
              <div style={{ fontSize: 11, color: "var(--color-text-tertiary)", marginTop: 1 }}>
                {p.category} · {p.elo_value} ELO
              </div>
            </div>
          </div>
          <div style={{
            fontSize: 13,
            fontWeight: 600,
            color: p.correct ? "#10B981" : "#EF4444",
            fontFamily: "monospace",
            minWidth: 48,
            textAlign: "right",
          }}>
            {p.delta > 0 ? `+${p.delta}` : p.delta}
          </div>
        </div>
      ))}
    </div>
  );
}

// ─── Componente principal ──────────────────────────────────────────────────────

export default function ELODashboard() {
  const { profile, history, loading } = useEloData();

  if (loading) {
    return (
      <div style={{ padding: 32, color: "var(--color-text-secondary)", fontSize: 14 }}>
        Cargando perfil ELO...
      </div>
    );
  }

  // Demo fallback cuando no hay datos reales
  const elo = profile?.elo_rating ?? 1250;
  const rank = profile?.rank ?? "Scholar";
  const rankColor = profile?.rank_color ?? "#3B82F6";

  return (
    <div style={{ padding: "24px 0", display: "flex", flexDirection: "column", gap: 20, maxWidth: 800 }}>

      {/* ELO Meter */}
      <EloMeter elo={elo} rank={rank} color={rankColor} />

      {/* Stats */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 }}>
        <StatCard
          label="ELO máximo"
          value={profile?.elo_peak ?? elo}
          sub="histórico"
        />
        <StatCard
          label="Precisión"
          value={`${profile?.accuracy ?? 0}%`}
          sub={`${profile?.puzzles_correct ?? 0} / ${profile?.puzzles_attempted ?? 0}`}
        />
        <StatCard
          label="Racha actual"
          value={profile?.streak_current ?? 0}
          sub={`mejor: ${profile?.streak_best ?? 0}`}
        />
        <StatCard
          label="Puzzles"
          value={profile?.puzzles_attempted ?? 0}
          sub="intentados"
        />
      </div>

      {/* Gráfica */}
      <EloChart history={history} />

      {/* Tabla de ranks + Actividad */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <RankTable userElo={elo} />
        <RecentActivity history={history} />
      </div>

    </div>
  );
}

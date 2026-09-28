import { Activity, Bell, CircleDollarSign, RadioTower, ShieldCheck, Zap } from "lucide-react";
import { EquityChart } from "@/components/EquityChart";

const health = [
  { label: "Data Feed", ok: true, icon: RadioTower },
  { label: "Broker", ok: true, icon: Zap },
  { label: "Risk Engine", ok: true, icon: ShieldCheck }
];

const trades = [
  {
    symbol: "RELIANCE",
    side: "BUY",
    entry: 2840.5,
    current: 2862.2,
    stop: 2818,
    target: 2895,
    reason: "ORB Breakout + Vol Spike"
  },
  {
    symbol: "HDFCBANK",
    side: "BUY",
    entry: 1518.1,
    current: 1524.8,
    stop: 1506.4,
    target: 1544,
    reason: "EMA Pullback + Trend Filter"
  }
];

function tradeProgress(trade: (typeof trades)[number]) {
  const total = trade.target - trade.stop;
  return Math.max(0, Math.min(100, ((trade.current - trade.stop) / total) * 100));
}

export default function Home() {
  return (
    <main className="min-h-screen bg-bg px-5 py-5 text-ink lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-5">
        <header className="flex flex-col gap-4 border-b border-line pb-5 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-wide text-mint">Paper Mode</p>
            <h1 className="text-3xl font-semibold tracking-normal">Trade Command Center</h1>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {health.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.label}
                  className="flex min-w-36 items-center gap-3 rounded-lg border border-line bg-panel px-4 py-3"
                >
                  <Icon className="h-5 w-5 text-muted" />
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${item.ok ? "bg-mint" : "bg-red"}`}
                    aria-hidden
                  />
                  <span className="text-sm text-muted">{item.label}</span>
                </div>
              );
            })}
          </div>
        </header>

        <section className="grid gap-4 lg:grid-cols-4">
          <Metric icon={CircleDollarSign} label="Live P&L" value="+₹12,900" tone="mint" />
          <Metric icon={Activity} label="Active Trades" value="2" tone="ink" />
          <Metric icon={ShieldCheck} label="Risk Used" value="0.8%" tone="amber" />
          <Metric icon={Bell} label="Alerts Today" value="0" tone="ink" />
        </section>

        <section className="grid gap-5 lg:grid-cols-[1.4fr_0.9fr]">
          <div className="rounded-lg border border-line bg-panel p-5">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold">30 Day Equity Curve</h2>
                <p className="text-sm text-muted">Capital growth and drawdown pressure</p>
              </div>
              <span className="rounded-md bg-panelSoft px-3 py-1 text-sm text-mint">+1.29%</span>
            </div>
            <EquityChart />
          </div>

          <div className="rounded-lg border border-line bg-panel p-5">
            <h2 className="mb-4 text-lg font-semibold">Signal Stream</h2>
            <div className="space-y-3">
              {["RELIANCE BUY validated", "Risk accepted: qty 222", "Paper order placed"].map(
                (event) => (
                  <div
                    key={event}
                    className="flex items-center justify-between border-b border-line pb-3 text-sm last:border-0"
                  >
                    <span>{event}</span>
                    <span className="text-muted">09:46</span>
                  </div>
                )
              )}
            </div>
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-2">
          {trades.map((trade) => (
            <article key={trade.symbol} className="rounded-lg border border-line bg-panel p-5">
              <div className="mb-4 flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-semibold">{trade.symbol}</h2>
                    <span className="rounded-md bg-mint px-2 py-1 text-xs font-bold text-bg">
                      {trade.side}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-muted">{trade.reason}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-muted">Current</p>
                  <p className="text-xl font-semibold">₹{trade.current.toFixed(2)}</p>
                </div>
              </div>

              <div className="mb-3 grid grid-cols-3 gap-3 text-sm">
                <Price label="SL" value={trade.stop} tone="red" />
                <Price label="Entry" value={trade.entry} tone="muted" />
                <Price label="Target" value={trade.target} tone="mint" />
              </div>

              <div className="h-3 overflow-hidden rounded-full bg-panelSoft">
                <div className="h-full bg-mint" style={{ width: `${tradeProgress(trade)}%` }} />
              </div>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}

function Metric({
  icon: Icon,
  label,
  value,
  tone
}: {
  icon: typeof Activity;
  label: string;
  value: string;
  tone: "mint" | "amber" | "ink";
}) {
  const toneClass = tone === "mint" ? "text-mint" : tone === "amber" ? "text-amber" : "text-ink";
  return (
    <div className="rounded-lg border border-line bg-panel p-5">
      <Icon className="mb-4 h-5 w-5 text-muted" />
      <p className="text-sm text-muted">{label}</p>
      <p className={`mt-1 text-2xl font-semibold ${toneClass}`}>{value}</p>
    </div>
  );
}

function Price({
  label,
  value,
  tone
}: {
  label: string;
  value: number;
  tone: "red" | "muted" | "mint";
}) {
  const toneClass = tone === "red" ? "text-red" : tone === "mint" ? "text-mint" : "text-muted";
  return (
    <div className="rounded-md bg-panelSoft p-3">
      <p className={`text-xs uppercase tracking-wide ${toneClass}`}>{label}</p>
      <p className="mt-1 font-semibold">₹{value.toFixed(2)}</p>
    </div>
  );
}


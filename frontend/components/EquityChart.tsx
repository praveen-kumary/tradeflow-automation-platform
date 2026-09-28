"use client";

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { date: "Apr 22", equity: 1000000 },
  { date: "Apr 23", equity: 1006400 },
  { date: "Apr 24", equity: 1003700 },
  { date: "Apr 25", equity: 1008900 },
  { date: "Apr 26", equity: 1007100 },
  { date: "Apr 27", equity: 1012900 }
];

export function EquityChart() {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={data} margin={{ top: 8, right: 0, bottom: 0, left: 0 }}>
        <defs>
          <linearGradient id="equity" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#58d68d" stopOpacity={0.42} />
            <stop offset="95%" stopColor="#58d68d" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis dataKey="date" stroke="#9eb5aa" tickLine={false} axisLine={false} />
        <YAxis
          stroke="#9eb5aa"
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${Number(value / 100000).toFixed(1)}L`}
          width={48}
        />
        <Tooltip
          contentStyle={{ background: "#101916", border: "1px solid #273832", borderRadius: 8 }}
          labelStyle={{ color: "#f5fff9" }}
          formatter={(value) => [`₹${Number(value).toLocaleString("en-IN")}`, "Equity"]}
        />
        <Area
          type="monotone"
          dataKey="equity"
          stroke="#58d68d"
          strokeWidth={2}
          fill="url(#equity)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}


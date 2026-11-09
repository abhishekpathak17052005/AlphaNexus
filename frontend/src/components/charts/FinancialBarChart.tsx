import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from 'recharts';

interface FinancialBarChartProps {
  data: {
    period: string;
    revenue: number;
    ebitda?: number;
    net_profit?: number;
  }[];
}

export const FinancialBarChart: React.FC<FinancialBarChartProps> = ({ data }) => {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 15, right: 15, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.2} vertical={false} />
          <XAxis dataKey="period" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis
            stroke="#64748b"
            fontSize={11}
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k Cr`}
          />
          <Tooltip
            content={({ active, payload, label }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl text-xs font-mono space-y-1">
                    <div className="text-slate-300 font-bold border-b border-slate-700 pb-1 mb-1">{label}</div>
                    {payload.map((entry) => (
                      <div key={entry.name} className="flex justify-between gap-4">
                        <span style={{ color: entry.color }}>{entry.name}:</span>
                        <span className="font-semibold text-slate-100">
                          ₹{Number(entry.value).toLocaleString('en-IN')} Cr
                        </span>
                      </div>
                    ))}
                  </div>
                );
              }
              return null;
            }}
          />
          <Legend
            verticalAlign="top"
            align="right"
            iconType="circle"
            wrapperStyle={{ paddingBottom: '10px', fontSize: '11px' }}
          />
          <Bar dataKey="revenue" name="Revenue" fill="#06b6d4" radius={[4, 4, 0, 0]} />
          <Bar dataKey="ebitda" name="EBITDA" fill="#10b981" radius={[4, 4, 0, 0]} />
          <Bar dataKey="net_profit" name="Net Profit (PAT)" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};


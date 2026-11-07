import React, { useState } from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

interface MarketChartProps {
  title?: string;
  data?: { time: string; value: number }[];
  isGain?: boolean;
}

const DEFAULT_CHART_DATA = [
  { time: '09:15', value: 24320 },
  { time: '10:00', value: 24360 },
  { time: '11:00', value: 24310 },
  { time: '12:00', value: 24420 },
  { time: '13:00', value: 24390 },
  { time: '14:00', value: 24470 },
  { time: '15:00', value: 24495 },
  { time: '15:30', value: 24530 },
];

export const MarketChart: React.FC<MarketChartProps> = ({
  data = DEFAULT_CHART_DATA,
  isGain = true,
}) => {
  const [timeframe, setTimeframe] = useState<'1D' | '1W' | '1M' | '1Y' | '5Y'>('1D');

  const strokeColor = isGain ? '#10b981' : '#f43f5e';
  const fillColor = isGain ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)';

  return (
    <div className="w-full flex flex-col">
      {/* Timeframe selector */}
      <div className="flex items-center justify-end gap-1 mb-3">
        {(['1D', '1W', '1M', '1Y', '5Y'] as const).map((tf) => (
          <button
            key={tf}
            onClick={() => setTimeframe(tf)}
            className={`px-2 py-0.5 text-xs font-mono rounded transition-colors ${
              timeframe === tf
                ? 'bg-cyan-500 text-white font-semibold shadow-xs'
                : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            }`}
          >
            {tf}
          </button>
        ))}
      </div>

      <div className="h-64 sm:h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={strokeColor} stopOpacity={0.3} />
                <stop offset="95%" stopColor={strokeColor} stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.2} vertical={false} />
            <XAxis
              dataKey="time"
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              domain={['auto', 'auto']}
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => v.toLocaleString('en-IN')}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-slate-900 border border-slate-700 p-2.5 rounded shadow-lg text-xs font-mono">
                      <div className="text-slate-400">{payload[0].payload.time}</div>
                      <div className="text-cyan-400 font-bold text-sm">
                        ₹{Number(payload[0].value).toLocaleString('en-IN')}
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke={strokeColor}
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#chartGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};


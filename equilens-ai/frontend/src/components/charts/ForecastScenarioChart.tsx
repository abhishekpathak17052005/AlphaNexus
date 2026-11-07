import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  Area,
} from 'recharts';

interface ForecastScenarioChartProps {
  historicalData: { period: string; value: number }[];
  forecastData: {
    period: string;
    base: number;
    bullish: number;
    bearish: number;
    confidence_intervals?: {
      ci_95: { lower: number; upper: number };
    };
  }[];
  metricLabel?: string;
  unit?: string;
}

export const ForecastScenarioChart: React.FC<ForecastScenarioChartProps> = ({
  historicalData,
  forecastData,
  metricLabel = 'Revenue',
  unit = '₹ Cr',
}) => {
  // Combine historical and forecast sequences seamlessly
  const combinedData: any[] = [];

  historicalData.forEach((h) => {
    combinedData.push({
      period: h.period,
      historical: h.value,
      base: null,
      bullish: null,
      bearish: null,
      isForecast: false,
    });
  });

  if (historicalData.length > 0 && forecastData.length > 0) {
    const lastHist = historicalData[historicalData.length - 1];
    combinedData[combinedData.length - 1] = {
      ...combinedData[combinedData.length - 1],
      base: lastHist.value,
      bullish: lastHist.value,
      bearish: lastHist.value,
    };
  }

  forecastData.forEach((f) => {
    combinedData.push({
      period: f.period,
      historical: null,
      base: f.base,
      bullish: f.bullish,
      bearish: f.bearish,
      ci_lower: f.confidence_intervals?.ci_95.lower,
      ci_upper: f.confidence_intervals?.ci_95.upper,
      isForecast: true,
    });
  });

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={combinedData} margin={{ top: 15, right: 20, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.2} vertical={false} />
          <XAxis dataKey="period" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis
            stroke="#64748b"
            fontSize={11}
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
          />
          <Tooltip
            content={({ active, payload, label }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl text-xs font-mono space-y-1">
                    <div className="text-slate-300 font-bold border-b border-slate-700 pb-1 mb-1">{label}</div>
                    {payload.map((entry) => {
                      if (entry.value === null) return null;
                      return (
                        <div key={entry.name} className="flex justify-between gap-4">
                          <span style={{ color: entry.color }}>{entry.name}:</span>
                          <span className="font-semibold text-slate-100">
                            ₹{Number(entry.value).toLocaleString('en-IN')} {unit}
                          </span>
                        </div>
                      );
                    })}
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

          {/* Historical Solid Line */}
          <Line
            type="monotone"
            dataKey="historical"
            name={`Historical ${metricLabel}`}
            stroke="#94a3b8"
            strokeWidth={3}
            dot={{ r: 4, fill: '#94a3b8' }}
          />

          {/* Forecast Scenarios */}
          <Line
            type="monotone"
            dataKey="bullish"
            name="Bullish Scenario (+15%)"
            stroke="#10b981"
            strokeWidth={2}
            strokeDasharray="4 4"
            dot={{ r: 3, fill: '#10b981' }}
          />
          <Line
            type="monotone"
            dataKey="base"
            name="Base Case Forecast"
            stroke="#06b6d4"
            strokeWidth={2.5}
            dot={{ r: 4, fill: '#06b6d4' }}
          />
          <Line
            type="monotone"
            dataKey="bearish"
            name="Bearish Scenario (-15%)"
            stroke="#f43f5e"
            strokeWidth={2}
            strokeDasharray="4 4"
            dot={{ r: 3, fill: '#f43f5e' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};


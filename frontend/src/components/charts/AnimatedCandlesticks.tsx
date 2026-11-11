import React, { useEffect, useRef, useState } from 'react';
import { motion, useAnimation } from 'motion/react';

/* ----------------------------------------------------------------
   Animated Candlestick Hero — AlphaNexus
   Decorative financial composition using SVG + Motion.
   This is NOT a live market chart. All values are illustrative.
   ---------------------------------------------------------------- */

interface Candle {
  x: number;
  open: number;
  close: number;
  high: number;
  low: number;
  bullish: boolean;
  delay: number;
}

// Illustrative demo candles — NOT real market prices
const CANDLES: Candle[] = [
  { x: 40,  open: 220, close: 180, high: 160, low: 240, bullish: false, delay: 0.0 },
  { x: 90,  open: 182, close: 148, high: 130, low: 200, bullish: false, delay: 0.1 },
  { x: 140, open: 150, close: 175, high: 125, low: 185, bullish: true,  delay: 0.2 },
  { x: 190, open: 173, close: 140, high: 120, low: 185, bullish: false, delay: 0.3 },
  { x: 240, open: 142, close: 108, high: 88,  low: 155, bullish: false, delay: 0.4 },
  { x: 290, open: 110, close: 142, high: 80,  low: 150, bullish: true,  delay: 0.5 },
  { x: 340, open: 140, close: 110, high: 90,  low: 155, bullish: false, delay: 0.6 },
  { x: 390, open: 112, close: 78,  high: 60,  low: 125, bullish: false, delay: 0.7 },
  { x: 440, open: 80,  close: 108, high: 55,  low: 115, bullish: true,  delay: 0.8 },
  { x: 490, open: 106, close: 72,  high: 55,  low: 115, bullish: false, delay: 0.9 },
  { x: 540, open: 74,  close: 108, high: 48,  low: 118, bullish: true,  delay: 1.0 },
  { x: 590, open: 106, close: 68,  high: 48,  low: 115, bullish: false, delay: 1.1 },
  { x: 640, open: 70,  close: 100, high: 44,  low: 110, bullish: true,  delay: 1.2 },
  { x: 690, open: 98,  close: 65,  high: 48,  low: 108, bullish: false, delay: 1.3 },
  { x: 740, open: 68,  close: 42,  high: 24,  low: 78,  bullish: false, delay: 1.4 },
  { x: 790, open: 44,  close: 72,  high: 20,  low: 82,  bullish: true,  delay: 1.5 },
  { x: 840, open: 70,  close: 44,  high: 26,  low: 80,  bullish: false, delay: 1.6 },
  { x: 890, open: 46,  close: 76,  high: 20,  low: 86,  bullish: true,  delay: 1.7 },
];

// Trend line through close prices (illustrative only)
function buildLinePath(candles: Candle[]): string {
  const points = candles.map((c) => `${c.x},${c.close}`);
  return `M${points.join(' L')}`;
}

const LINE_PATH = buildLinePath(CANDLES);
// Measure total path length for the dash animation
const APPROX_LINE_LENGTH = 900;

interface CandleStickProps {
  candle: Candle;
  index: number;
}

const CandleStick: React.FC<CandleStickProps> = ({ candle, index }) => {
  const { x, open, close, high, low, bullish, delay } = candle;
  const bodyTop = Math.min(open, close);
  const bodyHeight = Math.abs(open - close);
  const candleWidth = 20;
  const color = bullish ? 'var(--positive)' : 'var(--negative)';
  const strokeColor = bullish ? 'var(--positive-text)' : 'var(--negative-text)';

  return (
    <g>
      {/* Wick */}
      <motion.line
        x1={x} y1={high}
        x2={x} y2={low}
        stroke={color}
        strokeWidth={1.5}
        strokeLinecap="round"
        opacity={0.6}
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 0.6 }}
        transition={{ duration: 0.4, delay: delay + 0.25, ease: 'easeOut' }}
      />
      {/* Body */}
      <motion.rect
        x={x - candleWidth / 2}
        y={bodyTop}
        width={candleWidth}
        height={Math.max(bodyHeight, 2)}
        rx={3}
        fill={color}
        fillOpacity={0.85}
        initial={{ scaleY: 0, originY: `${bodyTop + bodyHeight}px` }}
        animate={{ scaleY: 1 }}
        style={{ transformOrigin: `${x}px ${bodyTop + bodyHeight}px` }}
        transition={{ duration: 0.5, delay, ease: [0.34, 1.56, 0.64, 1] }}
      />
      {/* Highlight rim */}
      <motion.rect
        x={x - candleWidth / 2}
        y={bodyTop}
        width={candleWidth}
        height={Math.max(bodyHeight, 2)}
        rx={3}
        fill="none"
        stroke={color}
        strokeWidth={1}
        strokeOpacity={0.5}
        initial={{ scaleY: 0 }}
        animate={{ scaleY: 1 }}
        style={{ transformOrigin: `${x}px ${bodyTop + bodyHeight}px` }}
        transition={{ duration: 0.5, delay, ease: [0.34, 1.56, 0.64, 1] }}
      />
    </g>
  );
};

export const AnimatedCandlesticks: React.FC = () => {
  const [animComplete, setAnimComplete] = useState(false);

  return (
    <div
      className="relative select-none"
      style={{ width: '100%', maxWidth: 960 }}
      aria-label="Decorative animated financial chart — illustrative data only"
      role="img"
    >
      {/* Floating container */}
      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
      >
        <svg
          viewBox="0 0 940 280"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style={{ width: '100%', height: 'auto', overflow: 'visible' }}
        >
          {/* Grid lines */}
          {[60, 120, 180, 240].map((y) => (
            <line
              key={y}
              x1="20" y1={y} x2="920" y2={y}
              stroke="var(--border)"
              strokeWidth={0.8}
              strokeDasharray="4 6"
            />
          ))}

          {/* Trend line */}
          <motion.path
            d={LINE_PATH}
            stroke="var(--brand)"
            strokeWidth={1.5}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
            strokeDasharray={APPROX_LINE_LENGTH}
            strokeDashoffset={APPROX_LINE_LENGTH}
            animate={{ strokeDashoffset: 0 }}
            transition={{ duration: 2.2, delay: 2.0, ease: 'easeInOut' }}
            opacity={0.7}
          />

          {/* Area fill under trend line */}
          <motion.path
            d={`${LINE_PATH} L${CANDLES[CANDLES.length - 1].x},280 L${CANDLES[0].x},280 Z`}
            fill="url(#areaGrad)"
            fillOpacity={0.12}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 2.5 }}
          />

          {/* Gradient defs */}
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#1558C9" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#1558C9" stopOpacity={0} />
            </linearGradient>
            <radialGradient id="glowBrand" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#1558C9" stopOpacity={0.25} />
              <stop offset="100%" stopColor="#1558C9" stopOpacity={0} />
            </radialGradient>
          </defs>

          {/* Candles */}
          {CANDLES.map((c, i) => (
            <CandleStick key={i} candle={c} index={i} />
          ))}

          {/* Lime highlight on last (highest) bullish candle */}
          <motion.rect
            x={790 - 10}
            y={20}
            width={20}
            height={52}
            rx={3}
            fill="var(--lime)"
            fillOpacity={0}
            animate={{ fillOpacity: [0, 0.25, 0.1] }}
            transition={{ delay: 3.5, duration: 1.2, repeat: Infinity, repeatDelay: 4 }}
          />

          {/* Lime dot on trend high */}
          <motion.circle
            cx={790}
            cy={20}
            r={4}
            fill="var(--lime)"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: [0, 1.4, 1], opacity: 1 }}
            transition={{ delay: 3.5, duration: 0.5 }}
          />
          <motion.circle
            cx={790}
            cy={20}
            r={8}
            fill="none"
            stroke="var(--lime)"
            strokeWidth={1.5}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: [0.5, 1.5, 1], opacity: [0, 0.6, 0] }}
            transition={{ delay: 3.5, duration: 1.2, repeat: Infinity, repeatDelay: 3 }}
          />

          {/* Price label */}
          <motion.g
            initial={{ opacity: 0, x: -4 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 3.8, duration: 0.4 }}
          >
            <rect x={800} y={10} width={72} height={22} rx={5} fill="var(--lime)" fillOpacity={0.15} stroke="var(--lime)" strokeWidth={1} strokeOpacity={0.4} />
            <text x={836} y={24} textAnchor="middle" fontSize={10} fill="var(--lime)" fontWeight="700" fontFamily="monospace">▲ HIGH</text>
          </motion.g>

          {/* Demo data label */}
          <motion.text
            x={470}
            y={270}
            textAnchor="middle"
            fontSize={9}
            fill="var(--text-4)"
            fontFamily="monospace"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 4, duration: 0.5 }}
          >
            ILLUSTRATIVE DATA — NOT REAL MARKET PRICES
          </motion.text>
        </svg>
      </motion.div>

      {/* Ambient glow */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse 60% 40% at 50% 60%, rgba(21,88,201,0.08) 0%, transparent 70%)',
        }}
      />
    </div>
  );
};

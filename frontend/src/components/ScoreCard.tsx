import React from 'react';

interface ScoreCardProps {
  title: string;
  score: number;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
}

const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  subtitle,
  icon,
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-success-600';
    if (score >= 60) return 'text-warning-600';
    return 'text-danger-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-success-100';
    if (score >= 60) return 'bg-warning-100';
    return 'bg-danger-100';
  };

  const getScoreRingColor = (score: number) => {
    if (score >= 80) return 'stroke-success-600';
    if (score >= 60) return 'stroke-warning-600';
    return 'stroke-danger-600';
  };

  return (
    <div className="metric-card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            {icon && <div className="text-gray-600">{icon}</div>}
            <h3 className="text-sm font-medium text-gray-600">{title}</h3>
          </div>

          <div className="flex items-baseline gap-2">
            <span className={`text-3xl font-bold ${getScoreColor(score)}`}>
              {score}
            </span>
            <span className="text-gray-500 text-sm">/100</span>
          </div>

          {subtitle && (
            <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>

        <div className="relative w-16 h-16">
          <svg className="w-16 h-16 transform -rotate-90">
            {/* Background circle */}
            <circle
              cx="32"
              cy="32"
              r="28"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
              className="text-gray-200"
            />
            {/* Progress circle */}
            <circle
              cx="32"
              cy="32"
              r="28"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
              strokeDasharray={`${2 * Math.PI * 28}`}
              strokeDashoffset={`${2 * Math.PI * 28 * (1 - score / 100)}`}
              className={`${getScoreRingColor(score)} transition-all duration-1000`}
              strokeLinecap="round"
            />
          </svg>
          <div
            className={`absolute inset-0 flex items-center justify-center ${getScoreBgColor(
              score
            )} rounded-full m-2`}
          >
            <span className={`text-xs font-semibold ${getScoreColor(score)}`}>
              {Math.round(score)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScoreCard;

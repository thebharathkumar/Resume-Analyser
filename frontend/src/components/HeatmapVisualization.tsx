import React from 'react';
import type { HeatmapData } from '../types/analysis';

interface HeatmapVisualizationProps {
  data: HeatmapData;
}

const HeatmapVisualization: React.FC<HeatmapVisualizationProps> = ({ data }) => {
  const getColorClass = (score: number) => {
    if (score >= 80) return 'bg-success-100 border-success-300 text-success-900';
    if (score >= 60) return 'bg-warning-100 border-warning-300 text-warning-900';
    if (score >= 40) return 'bg-orange-100 border-orange-300 text-orange-900';
    return 'bg-danger-100 border-danger-300 text-danger-900';
  };

  const getCategoryBadge = (category: string) => {
    const colors = {
      strong: 'bg-success-500',
      medium: 'bg-warning-500',
      weak: 'bg-danger-500',
    };

    return (
      <span className={`inline-block w-3 h-3 rounded-full ${colors[category as keyof typeof colors] || 'bg-gray-500'}`} />
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold text-gray-800">
          Grammar & Strength Heatmap
        </h3>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-success-500" />
            <span className="text-gray-600">Strong</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-warning-500" />
            <span className="text-gray-600">Medium</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-danger-500" />
            <span className="text-gray-600">Weak</span>
          </div>
        </div>
      </div>

      {/* Overall Score */}
      <div className="bg-gradient-to-r from-primary-50 to-purple-50 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Overall Grammar Score</p>
            <p className="text-3xl font-bold text-gray-800">
              {data.overall_grammar_score.toFixed(0)}
              <span className="text-lg text-gray-500">/100</span>
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Issues Found</p>
            <p className="text-2xl font-semibold text-danger-600">
              {data.grammar_issues.length}
            </p>
          </div>
        </div>
      </div>

      {/* Heatmap Sections */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {data.sections.map((section, index) => (
          <div
            key={index}
            className={`
              border-l-4 rounded-lg p-3 transition-all hover:shadow-md
              ${getColorClass(section.strength_score)}
            `}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-start gap-2 flex-1">
                <span className="text-xs font-mono text-gray-500 mt-1">
                  {section.line_number}
                </span>
                <div className="flex-1">
                  <p className="text-sm leading-relaxed">{section.text}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 flex-shrink-0">
                {getCategoryBadge(section.category)}
                <span className="text-xs font-semibold">
                  {section.strength_score.toFixed(0)}
                </span>
                {section.grammar_issues_count > 0 && (
                  <span className="text-xs bg-danger-500 text-white px-2 py-0.5 rounded-full">
                    {section.grammar_issues_count} issues
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Grammar Issues Details */}
      {data.grammar_issues.length > 0 && (
        <div className="mt-6">
          <h4 className="text-lg font-semibold text-gray-800 mb-3">
            Grammar Issues Details
          </h4>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {data.grammar_issues.slice(0, 10).map((issue, index) => (
              <div
                key={index}
                className="bg-white border border-gray-200 rounded-lg p-3 text-sm"
              >
                <div className="flex items-start justify-between mb-2">
                  <span
                    className={`
                    px-2 py-0.5 rounded text-xs font-medium
                    ${
                      issue.severity === 'error'
                        ? 'bg-danger-100 text-danger-700'
                        : issue.severity === 'warning'
                        ? 'bg-warning-100 text-warning-700'
                        : 'bg-blue-100 text-blue-700'
                    }
                  `}
                  >
                    {issue.severity}
                  </span>
                </div>

                <p className="text-gray-700 mb-2">{issue.message}</p>

                <div className="bg-gray-50 rounded p-2 mb-2">
                  <p className="text-gray-600 font-mono text-xs">
                    {issue.context}
                  </p>
                </div>

                {issue.suggestions.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Suggestions:</p>
                    <div className="flex flex-wrap gap-1">
                      {issue.suggestions.map((suggestion, idx) => (
                        <span
                          key={idx}
                          className="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded"
                        >
                          {suggestion}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HeatmapVisualization;

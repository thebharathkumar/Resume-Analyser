import React from 'react';
import type { KeywordAnalysis } from '../types/analysis';

interface KeywordAnalysisPanelProps {
  analysis: KeywordAnalysis;
}

const KeywordAnalysisPanel: React.FC<KeywordAnalysisPanelProps> = ({ analysis }) => {
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      programming: 'bg-blue-100 text-blue-700',
      web: 'bg-purple-100 text-purple-700',
      database: 'bg-green-100 text-green-700',
      cloud: 'bg-cyan-100 text-cyan-700',
      data_science: 'bg-pink-100 text-pink-700',
      soft_skills: 'bg-orange-100 text-orange-700',
      tools: 'bg-gray-100 text-gray-700',
      general: 'bg-gray-100 text-gray-600',
    };

    return colors[category] || colors.general;
  };

  // Group keywords by category
  const keywordsByCategory = analysis.matched_keywords.reduce((acc, keyword) => {
    if (!acc[keyword.category]) {
      acc[keyword.category] = [];
    }
    acc[keyword.category].push(keyword);
    return acc;
  }, {} as Record<string, typeof analysis.matched_keywords>);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="section-title">Keyword Analysis</h3>
        <div className="text-right">
          <p className="text-sm text-gray-600">Total Keywords</p>
          <p className="text-2xl font-bold text-gray-800">
            {analysis.total_keywords}
          </p>
        </div>
      </div>

      {/* Keywords by Category */}
      <div className="space-y-4">
        {Object.entries(keywordsByCategory).map(([category, keywords]) => (
          <div key={category} className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-semibold text-gray-700 mb-3 capitalize">
              {category.replace(/_/g, ' ')} ({keywords.length})
            </h4>
            <div className="flex flex-wrap gap-2">
              {keywords.map((keyword, index) => (
                <div
                  key={index}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium ${getCategoryColor(
                    category
                  )}`}
                >
                  <span>{keyword.keyword}</span>
                  {keyword.count > 1 && (
                    <span className="ml-1 opacity-70">×{keyword.count}</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Missing Keywords */}
      {analysis.missing_keywords.length > 0 && (
        <div className="bg-danger-50 border border-danger-200 rounded-lg p-4">
          <h4 className="font-semibold text-danger-800 mb-3">
            Missing Keywords (Add These!)
          </h4>
          <div className="flex flex-wrap gap-2">
            {analysis.missing_keywords.map((keyword, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-white text-danger-700 text-sm rounded border border-danger-300"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {analysis.recommendations.length > 0 && (
        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <h4 className="font-semibold text-primary-800 mb-3">
            Keyword Recommendations
          </h4>
          <ul className="space-y-2">
            {analysis.recommendations.map((recommendation, index) => (
              <li
                key={index}
                className="text-sm text-gray-700 flex items-start gap-2"
              >
                <span className="text-primary-600">→</span>
                <span>{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default KeywordAnalysisPanel;

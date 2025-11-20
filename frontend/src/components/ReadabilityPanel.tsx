import React from 'react';
import type { ReadabilityScore } from '../types/analysis';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

interface ReadabilityPanelProps {
  readability: ReadabilityScore;
}

const ReadabilityPanel: React.FC<ReadabilityPanelProps> = ({ readability }) => {
  const metrics = [
    {
      name: 'Flesch Reading Ease',
      value: readability.flesch_reading_ease,
      ideal: '60-70',
    },
    {
      name: 'Flesch-Kincaid Grade',
      value: readability.flesch_kincaid_grade,
      ideal: '10-14',
    },
    {
      name: 'Gunning Fog',
      value: readability.gunning_fog,
      ideal: '12-16',
    },
    {
      name: 'SMOG Index',
      value: readability.smog_index,
      ideal: '12-16',
    },
  ];

  const chartData = metrics.map((metric) => ({
    name: metric.name.split(' ')[0],
    score: Math.round(metric.value),
  }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="section-title">Readability Analysis</h3>
        <div className="text-right">
          <p className="text-sm text-gray-600">Hiring Manager Score</p>
          <p className="text-3xl font-bold text-gray-800">
            {readability.overall_score.toFixed(0)}
            <span className="text-lg text-gray-500">/100</span>
          </p>
        </div>
      </div>

      {/* Interpretation */}
      <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-4">
        <p className="text-gray-700">{readability.interpretation}</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => (
          <div
            key={index}
            className="bg-white border border-gray-200 rounded-lg p-4"
          >
            <p className="text-xs text-gray-500 mb-1">{metric.name}</p>
            <p className="text-2xl font-bold text-gray-800">
              {metric.value.toFixed(1)}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Ideal: {metric.ideal}
            </p>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="font-semibold text-gray-700 mb-4">
          Readability Metrics Visualization
        </h4>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="score" fill="#0ea5e9" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Recommendations */}
      {readability.recommendations.length > 0 && (
        <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
          <h4 className="font-semibold text-warning-800 mb-3">
            Readability Recommendations
          </h4>
          <ul className="space-y-2">
            {readability.recommendations.map((recommendation, index) => (
              <li
                key={index}
                className="text-sm text-gray-700 flex items-start gap-2"
              >
                <span className="text-warning-600">→</span>
                <span>{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ReadabilityPanel;

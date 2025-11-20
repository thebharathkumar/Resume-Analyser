import React from 'react';
import {
  ChartBarIcon,
  DocumentMagnifyingGlassIcon,
  SparklesIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  LightBulbIcon,
} from '@heroicons/react/24/outline';
import type { ResumeAnalysisResult } from '../types/analysis';
import ScoreCard from './ScoreCard';
import HeatmapVisualization from './HeatmapVisualization';
import KeywordAnalysisPanel from './KeywordAnalysisPanel';
import ReadabilityPanel from './ReadabilityPanel';

interface ResultsDashboardProps {
  result: ResumeAnalysisResult;
  onExportPDF?: () => void;
  onExportJSON?: () => void;
}

const ResultsDashboard: React.FC<ResultsDashboardProps> = ({
  result,
  onExportPDF,
  onExportJSON,
}) => {
  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Resume Analysis Results
            </h1>
            <p className="text-gray-600">
              {result.filename} • {result.word_count} words • {result.page_count}{' '}
              {result.page_count === 1 ? 'page' : 'pages'}
            </p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={onExportJSON}
              className="btn btn-secondary text-sm"
            >
              Export JSON
            </button>
            <button
              onClick={onExportPDF}
              className="btn btn-primary text-sm"
            >
              Export PDF
            </button>
          </div>
        </div>

        {/* Overall Score */}
        <div className="bg-gradient-to-r from-primary-500 to-purple-600 rounded-xl p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100 mb-2">Overall ATS Score</p>
              <p className="text-6xl font-bold">{result.overall_score.toFixed(0)}</p>
              <p className="text-primary-100 mt-2">out of 100</p>
            </div>

            <div className="text-right">
              <div className="bg-white/10 backdrop-blur rounded-lg p-4">
                <p className="text-sm text-primary-100 mb-2">Analysis ID</p>
                <p className="text-xs font-mono">{result.analysis_id.slice(0, 16)}...</p>
                <p className="text-xs text-primary-200 mt-2">
                  {new Date(result.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <ScoreCard
          title="ATS Compatibility"
          score={result.ats_compatibility.overall_score}
          subtitle="How well ATS can parse your resume"
          icon={<DocumentMagnifyingGlassIcon className="w-5 h-5" />}
        />

        <ScoreCard
          title="Keyword Match"
          score={result.keyword_analysis.overall_score}
          subtitle={`${result.keyword_analysis.total_keywords} keywords found`}
          icon={<SparklesIcon className="w-5 h-5" />}
        />

        <ScoreCard
          title="Grammar & Writing"
          score={result.heatmap_data.overall_grammar_score}
          subtitle={`${result.heatmap_data.grammar_issues.length} issues detected`}
          icon={<ChartBarIcon className="w-5 h-5" />}
        />

        <ScoreCard
          title="Readability"
          score={result.readability.overall_score}
          subtitle="Hiring manager friendliness"
          icon={<ChartBarIcon className="w-5 h-5" />}
        />
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircleIcon className="w-6 h-6 text-success-600" />
            <h3 className="text-xl font-bold text-gray-800">Strengths</h3>
          </div>
          <ul className="space-y-2">
            {result.strengths.map((strength, index) => (
              <li
                key={index}
                className="flex items-start gap-2 text-sm text-gray-700"
              >
                <span className="text-success-600 mt-0.5">✓</span>
                <span>{strength}</span>
              </li>
            ))}
            {result.strengths.length === 0 && (
              <p className="text-gray-500 text-sm">
                Analyze with job description for detailed strengths
              </p>
            )}
          </ul>
        </div>

        {/* Weaknesses */}
        <div className="card">
          <div className="flex items-center gap-2 mb-4">
            <ExclamationTriangleIcon className="w-6 h-6 text-warning-600" />
            <h3 className="text-xl font-bold text-gray-800">Areas to Improve</h3>
          </div>
          <ul className="space-y-2">
            {result.weaknesses.map((weakness, index) => (
              <li
                key={index}
                className="flex items-start gap-2 text-sm text-gray-700"
              >
                <span className="text-warning-600 mt-0.5">!</span>
                <span>{weakness}</span>
              </li>
            ))}
            {result.weaknesses.length === 0 && (
              <p className="text-success-600 text-sm">
                No major weaknesses detected! Great job!
              </p>
            )}
          </ul>
        </div>
      </div>

      {/* Priority Improvements */}
      {result.priority_improvements.length > 0 && (
        <div className="card bg-gradient-to-br from-warning-50 to-orange-50 border-2 border-warning-200">
          <div className="flex items-center gap-2 mb-4">
            <LightBulbIcon className="w-6 h-6 text-warning-600" />
            <h3 className="text-xl font-bold text-gray-800">
              Priority Improvements
            </h3>
          </div>
          <ol className="space-y-3">
            {result.priority_improvements.map((improvement, index) => (
              <li
                key={index}
                className="flex items-start gap-3 text-sm text-gray-700 bg-white rounded-lg p-3"
              >
                <span className="flex-shrink-0 w-6 h-6 bg-warning-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                  {index + 1}
                </span>
                <span className="flex-1">{improvement}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* Detailed Analysis Sections */}
      <div className="space-y-8">
        {/* ATS Compatibility Details */}
        <div className="card">
          <h3 className="section-title">ATS Compatibility Analysis</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Formatting</p>
              <p className="text-2xl font-bold text-gray-800">
                {result.ats_compatibility.formatting_score.toFixed(0)}
              </p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Structure</p>
              <p className="text-2xl font-bold text-gray-800">
                {result.ats_compatibility.structure_score.toFixed(0)}
              </p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Keyword Density</p>
              <p className="text-2xl font-bold text-gray-800">
                {result.ats_compatibility.keyword_density.toFixed(1)}%
              </p>
            </div>
          </div>

          {result.ats_compatibility.issues.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-700 mb-2">Issues:</h4>
              <ul className="space-y-1">
                {result.ats_compatibility.issues.map((issue, index) => (
                  <li key={index} className="text-sm text-danger-600 flex items-start gap-2">
                    <span>•</span>
                    <span>{issue}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.ats_compatibility.recommendations.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-700 mb-2">Recommendations:</h4>
              <ul className="space-y-1">
                {result.ats_compatibility.recommendations.map((rec, index) => (
                  <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                    <span>→</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Keywords */}
        <div className="card">
          <KeywordAnalysisPanel analysis={result.keyword_analysis} />
        </div>

        {/* Heatmap */}
        <div className="card">
          <HeatmapVisualization data={result.heatmap_data} />
        </div>

        {/* Readability */}
        <div className="card">
          <ReadabilityPanel readability={result.readability} />
        </div>

        {/* Role Matching */}
        {result.role_matching && (
          <div className="card">
            <h3 className="section-title">Role Match: {result.role_matching.target_role}</h3>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Overall Match</p>
                <p className="text-2xl font-bold text-gray-800">
                  {result.role_matching.match_percentage.toFixed(0)}%
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Experience</p>
                <p className="text-2xl font-bold text-gray-800">
                  {result.role_matching.experience_match.toFixed(0)}%
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Education</p>
                <p className="text-2xl font-bold text-gray-800">
                  {result.role_matching.education_match.toFixed(0)}%
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Skills Matched</p>
                <p className="text-2xl font-bold text-gray-800">
                  {result.role_matching.matched_skills.length}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-success-700 mb-2">Matched Skills:</h4>
                <div className="flex flex-wrap gap-2">
                  {result.role_matching.matched_skills.slice(0, 15).map((skill, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-success-100 text-success-700 text-xs rounded"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-danger-700 mb-2">Missing Skills:</h4>
                <div className="flex flex-wrap gap-2">
                  {result.role_matching.missing_skills.slice(0, 15).map((skill, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-danger-100 text-danger-700 text-xs rounded"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Job Description Comparison */}
        {result.job_comparison && (
          <div className="card">
            <h3 className="section-title">Job Description Comparison</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Match Score</p>
                <p className="text-3xl font-bold text-gray-800">
                  {result.job_comparison.match_score.toFixed(0)}%
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Keyword Overlap</p>
                <p className="text-3xl font-bold text-gray-800">
                  {result.job_comparison.keyword_overlap.toFixed(0)}%
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {result.job_comparison.missing_requirements.length > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">
                    Missing Requirements:
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {result.job_comparison.missing_requirements
                      .slice(0, 10)
                      .map((req, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-danger-100 text-danger-700 text-sm rounded"
                        >
                          {req}
                        </span>
                      ))}
                  </div>
                </div>
              )}

              {result.job_comparison.recommendations.length > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-700 mb-2">
                    Recommendations:
                  </h4>
                  <ul className="space-y-1">
                    {result.job_comparison.recommendations.map((rec, index) => (
                      <li
                        key={index}
                        className="text-sm text-gray-600 flex items-start gap-2"
                      >
                        <span>→</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDashboard;

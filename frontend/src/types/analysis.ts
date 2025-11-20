/**
 * TypeScript interfaces for Resume Analysis
 */

export interface KeywordMatch {
  keyword: string;
  count: number;
  relevance_score: number;
  category: string;
}

export interface KeywordAnalysis {
  total_keywords: number;
  matched_keywords: KeywordMatch[];
  missing_keywords: string[];
  overall_score: number;
  recommendations: string[];
}

export interface RoleMatch {
  target_role: string;
  match_percentage: number;
  matched_skills: string[];
  missing_skills: string[];
  experience_match: number;
  education_match: number;
  recommendations: string[];
}

export interface TextStrength {
  text: string;
  start_pos: number;
  end_pos: number;
  strength_score: number;
  category: 'strong' | 'medium' | 'weak';
  issues: string[];
  suggestions: string[];
}

export interface GrammarIssue {
  message: string;
  context: string;
  offset: number;
  length: number;
  rule_id: string;
  suggestions: string[];
  severity: 'error' | 'warning' | 'info';
}

export interface HeatmapData {
  sections: Array<{
    line_number: number;
    text: string;
    strength_score: number;
    grammar_issues_count: number;
    category: string;
  }>;
  text_strengths: TextStrength[];
  grammar_issues: GrammarIssue[];
  overall_grammar_score: number;
}

export interface ReadabilityScore {
  flesch_reading_ease: number;
  flesch_kincaid_grade: number;
  gunning_fog: number;
  smog_index: number;
  automated_readability_index: number;
  coleman_liau_index: number;
  overall_score: number;
  interpretation: string;
  recommendations: string[];
}

export interface ATSCompatibility {
  overall_score: number;
  formatting_score: number;
  structure_score: number;
  keyword_density: number;
  file_format_compatible: boolean;
  issues: string[];
  recommendations: string[];
}

export interface JobDescriptionComparison {
  match_score: number;
  matched_requirements: string[];
  missing_requirements: string[];
  keyword_overlap: number;
  skills_gap: string[];
  recommendations: string[];
}

export interface ResumeAnalysisResult {
  analysis_id: string;
  timestamp: string;
  filename: string;
  file_type: string;
  word_count: number;
  page_count: number;
  ats_compatibility: ATSCompatibility;
  keyword_analysis: KeywordAnalysis;
  role_matching: RoleMatch | null;
  heatmap_data: HeatmapData;
  readability: ReadabilityScore;
  job_comparison: JobDescriptionComparison | null;
  overall_score: number;
  strengths: string[];
  weaknesses: string[];
  priority_improvements: string[];
}

export interface UploadResponse {
  file_id: string;
  filename: string;
  file_type: string;
  size: number;
  message: string;
}

export interface AnalysisRequest {
  file_id: string;
  target_role?: string;
  job_description?: string;
  industry?: string;
}

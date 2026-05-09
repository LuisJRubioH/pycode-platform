export const TUTOR_CONTEXT_STORAGE_KEY = 'pycode_tutor_context'

export interface TutorContextPayload {
  problem_description?: string
  student_code?: string
  actual_output?: string
  expected_output?: string
  current_lesson?: string
  level?: string
  recent_errors?: string[]
  source?: string
  exercise_id?: number
}

export function saveTutorContext(context: TutorContextPayload) {
  localStorage.setItem(TUTOR_CONTEXT_STORAGE_KEY, JSON.stringify(context))
}

export function loadTutorContext(): TutorContextPayload | null {
  const raw = localStorage.getItem(TUTOR_CONTEXT_STORAGE_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw) as TutorContextPayload
  } catch {
    return null
  }
}

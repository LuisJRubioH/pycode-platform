import React, { useState } from 'react'

const TestAPI: React.FC = () => {
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  const getErrorMessage = (error: unknown) => {
    if (error instanceof Error) {
      return error.message
    }

    return String(error)
  }

  const testRegister = async () => {
    setLoading(true)
    setResult('')

    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'test@example.com',
          username: 'testuser',
          password: 'test123'
        })
      })

      const data = await response.json()
      setResult(`Status: ${response.status}\n${JSON.stringify(data, null, 2)}`)
    } catch (error) {
      setResult(`Error: ${getErrorMessage(error)}`)
    } finally {
      setLoading(false)
    }
  }

  const testHealth = async () => {
    setLoading(true)
    setResult('')

    try {
      const response = await fetch('/api/health')
      const data = await response.json()
      setResult(`Status: ${response.status}\n${JSON.stringify(data, null, 2)}`)
    } catch (error) {
      setResult(`Error: ${getErrorMessage(error)}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Test API Connection
          </h2>
        </div>
        <div className="space-y-4">
          <button
            onClick={testHealth}
            disabled={loading}
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            Test Health Endpoint
          </button>
          <button
            onClick={testRegister}
            disabled={loading}
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            Test Register Endpoint
          </button>
        </div>
        {result && (
          <div className="mt-8">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Result:</h3>
            <pre className="bg-white p-4 rounded border text-sm overflow-auto whitespace-pre-wrap">
              {result}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default TestAPI

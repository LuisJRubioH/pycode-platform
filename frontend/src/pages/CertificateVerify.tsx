import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ShieldCheck, ShieldX, Loader2 } from 'lucide-react'
import { api } from '../services/api'

interface VerifyResult {
  valid: boolean
  recipient_name: string | null
  title: string | null
  track: string | null
  issued_at: string | null
}

/**
 * Página PÚBLICA de verificación de un certificado por su código.
 * No requiere sesión: llama a GET /certificates/verify/{code} con skipAuth.
 * Es la URL impresa en el PDF para que un tercero (ej. reclutador) confirme
 * la autenticidad del certificado.
 */
const CertificateVerify: React.FC = () => {
  const { code } = useParams<{ code: string }>()
  const [result, setResult] = useState<VerifyResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const run = async () => {
      try {
        const res = await api.get(`/certificates/verify/${code}`, {
          skipAuth: true,
        })
        if (res.ok) {
          setResult(await res.json())
        } else {
          setResult({
            valid: false,
            recipient_name: null,
            title: null,
            track: null,
            issued_at: null,
          })
        }
      } catch {
        setResult({
          valid: false,
          recipient_name: null,
          title: null,
          track: null,
          issued_at: null,
        })
      } finally {
        setIsLoading(false)
      }
    }
    run()
  }, [code])

  const formatDate = (iso: string) =>
    new Date(iso).toLocaleDateString('es', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })

  return (
    <div className="max-w-xl mx-auto py-16 px-4">
      <div className="card p-8 text-center space-y-6">
        {isLoading ? (
          <div className="flex flex-col items-center gap-3 text-slate-500">
            <Loader2 className="h-10 w-10 animate-spin" />
            <p>Verificando certificado…</p>
          </div>
        ) : result?.valid ? (
          <>
            <div className="flex flex-col items-center gap-2">
              <ShieldCheck className="h-14 w-14 text-emerald-500" />
              <h1 className="text-2xl font-bold text-slate-900">
                Certificado válido
              </h1>
            </div>
            <div className="space-y-1">
              <p className="text-sm text-slate-500">Otorgado a</p>
              <p className="text-xl font-semibold text-slate-900">
                {result.recipient_name}
              </p>
            </div>
            <div className="border-t border-slate-200 pt-4 space-y-1">
              <p className="text-sm text-slate-500">Por completar</p>
              <p className="text-lg font-medium text-primary-600">
                {result.title}
              </p>
              {result.issued_at && (
                <p className="text-sm text-slate-500">
                  Emitido el {formatDate(result.issued_at)}
                </p>
              )}
            </div>
            <p className="text-xs text-slate-400 font-mono">{code}</p>
          </>
        ) : (
          <>
            <div className="flex flex-col items-center gap-2">
              <ShieldX className="h-14 w-14 text-rose-500" />
              <h1 className="text-2xl font-bold text-slate-900">
                Certificado no encontrado
              </h1>
            </div>
            <p className="text-slate-600">
              El código <span className="font-mono">{code}</span> no corresponde a
              ningún certificado emitido por PyCode Platform.
            </p>
          </>
        )}

        <Link
          to="/"
          className="inline-block text-sm text-primary-600 hover:text-primary-500"
        >
          ← Ir a PyCode Platform
        </Link>
      </div>
    </div>
  )
}

export default CertificateVerify

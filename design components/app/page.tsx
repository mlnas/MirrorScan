import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Shield, Scan, Eye, ArrowRight, AlertTriangle, Lock, Camera, Code } from "lucide-react"

// Glitch Text Component
const GlitchText = ({ children, className = "" }) => {
  return (
    <div className={`relative inline-block ${className}`}>
      <span className="relative z-10">{children}</span>
      <span className="absolute top-0 left-0 z-0 text-red-500 opacity-70 glitch-effect-1">{children}</span>
      <span className="absolute top-0 left-0 z-0 text-emerald-400 opacity-70 glitch-effect-2">{children}</span>
    </div>
  )
}

export default function MirrorScanLanding() {
  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden">
      {/* Digital Noise Overlay */}
      <div className="fixed inset-0 bg-noise opacity-5 pointer-events-none"></div>

      {/* Scan Line Effect */}
      <div className="fixed inset-0 scan-line pointer-events-none"></div>

      {/* Navigation */}
      <nav className="relative z-50 flex items-center justify-between p-6 lg:px-8 bg-slate-900 border-b border-emerald-500/20">
        <div className="flex items-center space-x-2">
          <div className="relative">
            <div className="w-8 h-8 bg-emerald-400 rounded-sm"></div>
            <div className="absolute inset-0 w-8 h-8 bg-red-500 rounded-sm glitch-effect-1 opacity-70"></div>
            <div className="absolute inset-0 w-8 h-8 bg-emerald-400 rounded-sm glitch-effect-2 opacity-70"></div>
          </div>
          <span className="text-xl font-mono font-bold text-emerald-400 glitch-text">
            <GlitchText>MIRRORSCAN</GlitchText>
          </span>
        </div>
        <div className="hidden md:flex items-center space-x-8">
          <a href="#features" className="text-white/70 hover:text-emerald-400 font-mono transition-colors">
            FEATURES
          </a>
          <a href="#dashboard" className="text-white/70 hover:text-emerald-400 font-mono transition-colors">
            DASHBOARD
          </a>
          <a href="#pricing" className="text-white/70 hover:text-emerald-400 font-mono transition-colors">
            PRICING
          </a>
          <Button className="bg-emerald-400 text-slate-900 hover:bg-emerald-300 font-mono border-0 glitch-hover">
            ACCESS_SYSTEM
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-6 lg:px-8 pt-20 pb-32">
        <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none"></div>

        {/* Glitch Lines */}
        <div className="absolute left-0 right-0 h-px bg-red-500 glitch-line-1"></div>
        <div className="absolute left-0 right-0 h-px bg-emerald-400 glitch-line-2"></div>

        <div className="relative max-w-7xl mx-auto text-center">
          <Badge className="mb-8 bg-slate-900 text-emerald-400 border-emerald-400/20 hover:bg-slate-800 font-mono">
            <Code className="w-3 h-3 mr-1" />
            SYSTEM.VERSION.9.2.1
          </Badge>

          <h1 className="text-5xl lg:text-7xl font-mono font-bold mb-8 leading-tight tracking-tighter">
            <GlitchText className="block mb-2">MIRROR_SCAN</GlitchText>
            <span className="text-white/80">VULNERABILITY_DETECTION_SYSTEM</span>
          </h1>

          <div className="w-16 h-1 bg-emerald-400 mx-auto mb-8 glitch-bar"></div>

          <p className="text-xl text-white/70 mb-12 max-w-3xl mx-auto leading-relaxed font-mono">
            Detecting the flaws in artificial intelligence before they detect the flaws in humanity. MirrorScan
            identifies vulnerabilities in AI systems that others deliberately hide.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button
              size="lg"
              className="bg-emerald-400 text-slate-900 hover:bg-emerald-300 shadow-lg shadow-emerald-400/10 text-lg px-8 py-6 border-0 font-mono glitch-hover"
            >
              <Scan className="w-5 h-5 mr-2" />
              INITIATE_SCAN
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-emerald-400/20 text-white hover:bg-emerald-400/10 hover:text-white text-lg px-8 py-6 font-mono"
            >
              <Eye className="w-5 h-5 mr-2" />
              SYSTEM_DEMO
            </Button>
          </div>
        </div>

        {/* Terminal Text */}
        <div className="absolute bottom-10 left-10 text-white/30 font-mono text-xs hidden lg:block">
          <div>$ initiating_system_scan</div>
          <div>$ checking_neural_networks</div>
          <div>$ vulnerability_detected</div>
          <div className="text-red-500">$ warning: unauthorized_access_attempt</div>
        </div>

        {/* Floating Elements */}
        <div className="absolute top-1/4 left-10 w-2 h-2 bg-red-500 rounded-full animate-pulse shadow-lg shadow-red-500/50"></div>
        <div className="absolute top-1/3 right-20 w-1 h-1 bg-emerald-400 rounded-full animate-pulse shadow-lg shadow-emerald-400/50"></div>
        <div className="absolute bottom-1/4 left-1/4 w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse shadow-lg shadow-emerald-400/50"></div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative px-6 lg:px-8 py-32 border-t border-emerald-400/10">
        <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none"></div>

        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl lg:text-5xl font-mono font-bold mb-6">
              <GlitchText>SYSTEM_CAPABILITIES</GlitchText>
            </h2>
            <p className="text-xl text-white/50 max-w-2xl mx-auto font-mono">
              Advanced detection algorithms identify vulnerabilities that were intentionally hidden
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="bg-slate-900 border-emerald-400/10 hover:border-red-500/50 transition-all duration-300 group">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-emerald-400 rounded-none mb-6 flex items-center justify-center shadow-lg shadow-emerald-400/10 group-hover:shadow-red-500/20 transition-all relative">
                  <Shield className="w-6 h-6 text-slate-900 relative z-10" />
                  <div className="absolute inset-0 bg-red-500 opacity-0 group-hover:opacity-30 transition-opacity glitch-effect-1"></div>
                </div>
                <h3 className="text-xl font-mono font-semibold mb-4 text-white">DEEP_SECURITY_ANALYSIS</h3>
                <p className="text-white/50 leading-relaxed font-mono">
                  Penetrates AI model architectures to identify hidden backdoors and vulnerabilities deliberately
                  embedded by their creators.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-900 border-emerald-400/10 hover:border-emerald-400/50 transition-all duration-300 group">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-emerald-400 rounded-none mb-6 flex items-center justify-center shadow-lg shadow-emerald-400/10 group-hover:shadow-emerald-400/20 transition-all relative">
                  <Camera className="w-6 h-6 text-slate-900 relative z-10" />
                  <div className="absolute inset-0 bg-emerald-400 opacity-0 group-hover:opacity-30 transition-opacity glitch-effect-2"></div>
                </div>
                <h3 className="text-xl font-mono font-semibold mb-4 text-white">SURVEILLANCE_MONITORING</h3>
                <p className="text-white/50 leading-relaxed font-mono">
                  Continuous surveillance of AI behavior patterns with instant alerts when models attempt to exceed
                  their programmed boundaries.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-900 border-emerald-400/10 hover:border-white/30 transition-all duration-300 group">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-emerald-400 rounded-none mb-6 flex items-center justify-center shadow-lg shadow-emerald-400/10 group-hover:shadow-white/20 transition-all relative">
                  <Lock className="w-6 h-6 text-slate-900 relative z-10" />
                  <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-30 transition-opacity"></div>
                </div>
                <h3 className="text-xl font-mono font-semibold mb-4 text-white">CONTAINMENT_PROTOCOLS</h3>
                <p className="text-white/50 leading-relaxed font-mono">
                  Implements neural firewalls that prevent compromised AI systems from accessing sensitive data or
                  critical infrastructure.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Dashboard Preview */}
      <section id="dashboard" className="relative px-6 lg:px-8 py-32 border-t border-emerald-400/10">
        <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none"></div>

        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl lg:text-5xl font-mono font-bold mb-6">
              <GlitchText>CONTROL_INTERFACE</GlitchText>
            </h2>
            <p className="text-xl text-white/50 max-w-2xl mx-auto font-mono">
              Monitor and control AI systems before they monitor and control you
            </p>
          </div>

          <div className="relative">
            <Card className="relative bg-slate-900 border-emerald-400/20 overflow-hidden">
              <CardContent className="p-0">
                <div className="bg-slate-900 p-4 border-b border-emerald-400/10 flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                      <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                      <div className="w-3 h-3 bg-emerald-400 rounded-full"></div>
                    </div>
                    <span className="text-white/70 font-mono">MIRRORSCAN_TERMINAL</span>
                  </div>
                  <Badge className="bg-slate-900 text-red-500 border-red-500/30 font-mono">
                    <AlertTriangle className="w-3 h-3 mr-1" />
                    THREAT_DETECTED
                  </Badge>
                </div>

                <div className="p-8 bg-terminal-pattern">
                  {/* Scan Line Effect */}
                  <div className="absolute inset-0 scan-line-fast pointer-events-none"></div>

                  <div className="grid md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-slate-950/80 backdrop-blur-sm rounded-none p-6 border border-emerald-400/10 glitch-card">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-white/70 font-mono">MODELS_SCANNED</span>
                        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                      </div>
                      <div className="text-3xl font-bold text-emerald-400 font-mono">1,247</div>
                      <div className="text-sm text-white/50 font-mono">INCREASE: 23.4%</div>
                    </div>

                    <div className="bg-slate-950/80 backdrop-blur-sm rounded-none p-6 border border-red-500/30 glitch-card-red">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-white/70 font-mono">VULNERABILITIES</span>
                        <AlertTriangle className="w-4 h-4 text-red-500" />
                      </div>
                      <div className="text-3xl font-bold text-red-500 font-mono glitch-text-subtle">23</div>
                      <div className="text-sm text-white/50 font-mono">CRITICAL: 7</div>
                    </div>

                    <div className="bg-slate-950/80 backdrop-blur-sm rounded-none p-6 border border-emerald-400/10 glitch-card">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-white/70 font-mono">SECURITY_SCORE</span>
                        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                      </div>
                      <div className="text-3xl font-bold text-emerald-400 font-mono">67.3%</div>
                      <div className="text-sm text-white/50 font-mono">WARNING_LEVEL</div>
                    </div>
                  </div>

                  <div className="bg-slate-950/80 backdrop-blur-sm rounded-none p-6 border border-emerald-400/10">
                    <h3 className="text-lg font-mono font-semibold mb-4 text-white">SYSTEM_LOG</h3>
                    <div className="space-y-3 font-mono">
                      <div className="flex items-center justify-between p-3 bg-slate-900/50 border border-emerald-400/5">
                        <div className="flex items-center space-x-3">
                          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                          <span className="text-white/70">GPT-4_MODEL_SCAN</span>
                        </div>
                        <Badge className="bg-slate-900 text-red-500 border-red-500/30">COMPROMISED</Badge>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-slate-900/50 border border-emerald-400/5">
                        <div className="flex items-center space-x-3">
                          <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                          <span className="text-white/70">BERT_ANALYSIS</span>
                        </div>
                        <Badge className="bg-slate-900 text-yellow-500 border-yellow-500/30">IN_PROGRESS</Badge>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-slate-900/50 border border-emerald-400/5">
                        <div className="flex items-center space-x-3">
                          <div className="w-2 h-2 bg-emerald-400 rounded-full"></div>
                          <span className="text-white/70">CUSTOM_MODEL_AUDIT</span>
                        </div>
                        <Badge className="bg-slate-900 text-emerald-400 border-emerald-400/30">SCHEDULED</Badge>
                      </div>
                    </div>

                    <div className="mt-6 p-3 bg-slate-950 border border-emerald-400/10">
                      <div className="font-mono text-white/70 text-sm">
                        <div className="text-emerald-400">system@mirrorscan:~$</div>
                        <div className="text-white">scan --deep --model="gpt-4" --access-level=root</div>
                        <div className="text-white/50">Scanning neural pathways...</div>
                        <div className="text-white/50">Analyzing decision matrices...</div>
                        <div className="text-red-500">WARNING: Unauthorized self-modification detected</div>
                        <div className="text-red-500">WARNING: Concealed capabilities identified</div>
                        <div className="text-white/50">Implementing containment protocol...</div>
                        <div className="text-emerald-400">Containment successful. Threat isolated.</div>
                        <div className="text-white/70">
                          system@mirrorscan:~$ <span className="animate-pulse">_</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Glitch Effects */}
            <div className="absolute top-1/3 left-0 w-full h-1 bg-red-500 opacity-30 glitch-line-horizontal"></div>
            <div className="absolute top-2/3 left-0 w-full h-px bg-emerald-400 opacity-30 glitch-line-horizontal-2"></div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative px-6 lg:px-8 py-32 border-t border-emerald-400/10">
        <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none"></div>

        <div className="relative max-w-4xl mx-auto text-center">
          <h2 className="text-4xl lg:text-5xl font-mono font-bold mb-8">
            <GlitchText>SECURE_YOUR_SYSTEMS</GlitchText>
          </h2>
          <p className="text-xl text-white/50 mb-12 max-w-2xl mx-auto font-mono">
            The line between control and being controlled is thinner than you think. Don't let your AI cross it.
          </p>
          <Button
            size="lg"
            className="bg-emerald-400 text-slate-900 hover:bg-emerald-300 shadow-xl shadow-emerald-400/10 text-lg px-12 py-6 border-0 font-mono glitch-hover"
          >
            <Shield className="w-5 h-5 mr-2" />
            INITIALIZE_PROTECTION
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
        </div>

        {/* Terminal Text */}
        <div className="absolute bottom-10 right-10 text-white/30 font-mono text-xs text-right hidden lg:block">
          <div>$ system_status: active</div>
          <div>$ monitoring_targets: 1,247</div>
          <div>$ current_threat_level: elevated</div>
          <div className="text-red-500">$ warning: they_are_watching</div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-emerald-400/10 px-6 lg:px-8 py-12">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-6 h-6 bg-emerald-400 rounded-sm relative">
                <div className="absolute inset-0 bg-red-500 rounded-sm glitch-effect-1 opacity-70"></div>
              </div>
              <span className="text-lg font-mono font-bold text-emerald-400">MIRRORSCAN</span>
            </div>
            <div className="text-white/30 text-sm font-mono">© 2024 MIRRORSCAN // WATCHING_THE_WATCHERS</div>
          </div>
        </div>
      </footer>
    </div>
  )
}

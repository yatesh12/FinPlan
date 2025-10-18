import { useState } from "react"
import { LayoutDashboard, Target, TrendingUp, User, Brain, PieChart } from "lucide-react"
import DashboardTab from "./Dashboard/dashboard-tab"
import { MarketAnalysisTab } from "./Dashboard/market-analysis-tab"
import { FinancialGoals } from "./Dashboard/financial-goals";
import ProfileTab from "./Dashboard/profile-tab"
import PortfolioTab from "./Dashboard/portfolio-tab"

const MainDashboard = ({ userData }) => {
  const [activeTab, setActiveTab] = useState("dashboard")

  const tabs = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "portfolio", label: "Portfolio", icon: PieChart },
    { id: "market", label: "Market Analysis", icon: TrendingUp },
    { id: "goals", label: "Financial Goals", icon: Target },
    { id: "ai-insights", label: "AI-Insights", icon: Brain },
    { id: "profile", label: "Profile", icon: User },
  ]

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <DashboardTab userData={userData} />
      case "portfolio":
        return <PortfolioTab />
      case "market":
        return <MarketAnalysisTab />
      case "goals":
        return <FinancialGoals />
      case "ai-insights":
        return (
          <div className="h-full w-full">
            <div className="w-full bg-white rounded-lg shadow-sm border" style={{ height: 'calc(100vh - 120px)' }}>
              <iframe 
                src="http://localhost:8502/?embedded=true" 
                width="100%" 
                height="100%"
                style={{ border: 'none', borderRadius: '8px' }}
                title="Local Streamlit AI Insights"
                sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
              />
            </div>
          </div>
        )
      case "profile":
        return <ProfileTab userData={userData} />
      default:
        return <DashboardTab userData={userData} />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white">
        <nav className="mt-8">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center px-6 py-3 text-left transition-colors ${
                  activeTab === tab.id
                    ? "bg-gray-800 text-white border-r-2 border-blue-500"
                    : "text-gray-300 hover:bg-gray-800 hover:text-white"
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {tab.label}
              </button>
            )
          })}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-8">{renderContent()}</div>
      </div>
    </div>
  )
}

export default MainDashboard

import { useState, useEffect } from "react"
import { DollarSign, TrendingUp, Target, Users, PiggyBank, Home, GraduationCap } from "lucide-react"
import { profileAPI } from "../../api/profile"

const DashboardTab = ({ userData }) => {
  const [profileData, setProfileData] = useState(null)

  useEffect(() => {
    loadProfileData()
  }, [])

  const loadProfileData = async () => {
    try {
      const response = await profileAPI.getProfile()
      if (response.success && response.profile) {
        setProfileData(response.profile)
      }
    } catch (error) {
      console.error('Error loading profile data:', error)
    }
  }

  const parseGoalData = () => {
    if (!profileData?.financial_goals) return { goalName: "N/A", targetAmount: 0, goalDate: null }
    
    try {
      // Try to parse as JSON (new format)
      const goals = JSON.parse(profileData.financial_goals)
      if (Array.isArray(goals) && goals.length > 0) {
        const primaryGoal = goals[0]
        return {
          goalName: primaryGoal.name || "N/A",
          targetAmount: primaryGoal.amount || 0,
          goalDate: primaryGoal.date || null
        }
      }
    } catch (e) {
      // If not JSON, assume it's text goals
      return {
        goalName: profileData.financial_goals,
        targetAmount: 50000, // default target
        goalDate: null
      }
    }
    
    return { goalName: "N/A", targetAmount: 0, goalDate: null }
  }

  const calculateGoalProgress = () => {
    if (!profileData) return { progress: "N/A", change: "No data" }
    
    const currentSavings = profileData.savings || 0
    const { targetAmount } = parseGoalData()
    
    if (targetAmount === 0) return { progress: "N/A", change: "No target set" }
    
    const progressPercent = Math.min(100, Math.round((currentSavings / targetAmount) * 100))
    return { progress: `${progressPercent}%`, change: `+${Math.round(progressPercent / 10)}%` }
  }
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "INR",
    }).format(amount)
  }

  const getGoalIcon = (goal) => {
    const goalLower = goal?.toLowerCase() || ""
    
    if (goalLower.includes("retirement")) {
      return <PiggyBank className="w-6 h-6 text-emerald-600" />
    }
    if (goalLower.includes("education") || goalLower.includes("child")) {
      return <GraduationCap className="w-6 h-6 text-indigo-600" />
    }
    if (goalLower.includes("home") || goalLower.includes("house") || goalLower.includes("buy")) {
      return <Home className="w-6 h-6 text-blue-600" />
    }
    if (goalLower.includes("car") || goalLower.includes("vehicle")) {
      return <Target className="w-6 h-6 text-purple-600" />
    }
    
    return <Target className="w-6 h-6 text-gray-600" />
  }

  const goalProgress = calculateGoalProgress()
  const goalData = parseGoalData()
  
  const stats = [
    {
      title: "Monthly Income",
      value: formatCurrency(profileData?.income || 0),
      icon: DollarSign,
      change: "+12.5%",
      positive: true,
    },
    {
      title: "Monthly Savings",
      value: formatCurrency(profileData?.savings || 0),
      icon: TrendingUp,
      change: "+8.2%",
      positive: true,
    },
    {
      title: "Goal Progress",
      value: goalProgress.progress,
      icon: Target,
      change: goalProgress.change,
      positive: goalProgress.progress !== "N/A",
    },
    {
      title: "Age",
      value: profileData?.age || "N/A",
      icon: Users,
      change: "No change",
      positive: null,
    },
  ]

  return (
    <div className="space-y-8">
      {/* Welcome */}
      <div className="text-center lg:text-left">
        <h2 className="text-3xl font-bold text-gray-900">
          Welcome Back!
        </h2>
        <p className="text-gray-600 mt-2 text-lg">Here’s your personalized financial dashboard</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div
              key={index}
              className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-md border border-gray-200 p-6 hover:shadow-lg transition"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                </div>
                <div className="bg-blue-100 p-3 rounded-xl">
                  <Icon className="w-6 h-6 text-blue-600" />
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm">
                <span
                  className={`font-medium ${
                    stat.positive === true
                      ? "text-green-600"
                      : stat.positive === false
                        ? "text-red-600"
                        : "text-gray-500"
                  }`}
                >
                  {stat.change}
                </span>
                <span className="text-gray-500 ml-2">from last month</span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Profile + Goal */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile Summary */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-100">
          <div className="p-6 border-b border-gray-100 flex items-center justify-between">
            <h3 className="text-lg font-semibold text-green-900 bg-green-100 rounded-2xl py-1 px-4 border border-green-300">Profile Summary</h3>
            <Users className="w-5 h-5 text-gray-400" />
          </div>
          <div className="p-6 grid grid-cols-2 gap-6">
            <div>
              <p className="text-gray-500">Age</p>
              <p className="font-semibold text-gray-900">
                {profileData?.age || "N/A"}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Income</p>
              <p className="font-semibold text-gray-900">
                {formatCurrency(profileData?.income || 0)}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Expenses</p>
              <p className="font-semibold text-gray-900">
                {formatCurrency(profileData?.expenses || 0)}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Risk Level</p>
              <p className="font-semibold text-gray-900 capitalize">{profileData?.risk_tolerance || "N/A"}</p>
            </div>
          </div>
        </div>

        {/* Primary Goal */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-100">
          <div className="p-6 border-b border-gray-100 flex items-center">
            {getGoalIcon(goalData.goalName)}
            <h3 className="ml-2 text-lg font-semibold text-green-900 bg-green-100 rounded-2xl py-1 px-4 border border-green-300">Primary Goal</h3>
          </div>
          <div className="p-6 space-y-4 text-sm">
            <div>
              <p className="text-gray-500">Goal Name</p>
              <p className="font-semibold text-gray-900 capitalize">
                {goalData.goalName}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Target Amount</p>
              <p className="font-semibold text-gray-900">{formatCurrency(goalData.targetAmount)}</p>
            </div>
            <div>
              <p className="text-gray-500">Current Savings</p>
              <p className="font-semibold text-gray-900">{formatCurrency(profileData?.savings || 0)}</p>
            </div>

            {/* Progress bar */}
            <div className="pt-2">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Progress</span>
                <span className="text-gray-900">{goalProgress.progress}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-gradient-to-r from-green-400 to-emerald-600 h-2 rounded-full" style={{ width: goalProgress.progress }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Financial Overview */}
      <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-md border border-gray-100">
        <div className="p-6 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-green-900 bg-green-100 rounded-2xl py-1 px-4 border border-green-300">Financial Overview</h3>
        </div>
        <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="p-4 rounded-lg hover:bg-gray-50 transition">
            <p className="text-sm text-gray-500">Monthly Income</p>
            <p className="text-2xl font-bold text-green-600 mt-1">
              {formatCurrency(profileData?.income || 0)}
            </p>
          </div>
          <div className="p-4 rounded-lg hover:bg-gray-50 transition">
            <p className="text-sm text-gray-500">Monthly Expenses</p>
            <p className="text-2xl font-bold text-red-600 mt-1">
              {formatCurrency(profileData?.expenses || 0)}
            </p>
          </div>
          <div className="p-4 rounded-lg hover:bg-gray-50 transition">
            <p className="text-sm text-gray-500">Monthly Savings</p>
            <p className="text-2xl font-bold text-blue-600 mt-1">
              {formatCurrency(profileData?.savings || 0)}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardTab

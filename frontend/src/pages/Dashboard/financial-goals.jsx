import { useState, useEffect, useCallback } from "react"
import { Target, Calendar, TrendingUp, PiggyBank, Home, Car, GraduationCap, Plane } from "lucide-react"
import { profileAPI } from "../../api/profile"

const assetAllocation = [
  { category: "Emergency Fund", percentage: 15, description: "3-6 months of expenses in liquid savings" },
  {
    category: "Equity Mutual Funds",
    percentage: 40,
    description: "Long-term wealth creation through diversified equity",
  },
  { category: "Debt Funds", percentage: 20, description: "Stable returns with lower risk" },
  { category: "PPF/ELSS", percentage: 15, description: "Tax-saving investments with long-term benefits" },
  { category: "Real Estate", percentage: 10, description: "Property investment for portfolio diversification" },
]

export function FinancialGoals() {
  const [profileData, setProfileData] = useState(null)
  const [userGoals, setUserGoals] = useState([])
  const [loading, setLoading] = useState(true)

  const getGoalIcon = useCallback((goalName) => {
  if (!goalName) return Target;

  const name = goalName.toLowerCase();
  if (name.includes("home") || name.includes("house")) return Home;
  if (name.includes("car") || name.includes("vehicle")) return Car;
  if (name.includes("education") || name.includes("study")) return GraduationCap;
  if (name.includes("vacation") || name.includes("travel")) return Plane;
  if (name.includes("emergency") || name.includes("fund")) return PiggyBank;

  return Target;
}, []); // no dependencies → stable across renders

const getGoalColor = useCallback((index) => {
  const colors = [
    "bg-blue-500",
    "bg-green-500",
    "bg-orange-500",
    "bg-purple-500",
    "bg-pink-500",
  ];
  return colors[index % colors.length];
}, []);

  const parseUserGoals = useCallback(
  (financialGoals, profile) => {
    console.log("Parsing financial goals:", financialGoals);
    console.log("Profile data:", profile);
    
    if (!financialGoals) {
      console.log("No financial goals found");
      setUserGoals([]);
      return;
  }

    const currentSavings = profile?.savings || 0;
    console.log("Current savings:", currentSavings);

      try {
        const goals = JSON.parse(financialGoals);
        console.log("Parsed goals:", goals);
        if (Array.isArray(goals)) {
          const parsedGoals = goals.map((goal, index) => ({
            id: goal.id || index + 1,
            title: goal.name || "Financial Goal",
            target: goal.amount || 0,
            current: currentSavings,
            deadline: goal.date
              ? new Date(goal.date).toLocaleDateString("en-US", {
                  month: "short",
                  year: "numeric",
                })
              : "N/A",
            category: goal.type || "General",
            icon: getGoalIcon(goal.name || ""),
            color: getGoalColor(index),
          }));
          setUserGoals(parsedGoals);
        } else {
          // Text-based goal
          setUserGoals([
            {
              id: 1,
              title: financialGoals,
              target: 50000,
              current: currentSavings,
              deadline: "N/A",
              category: "General",
              icon: Target,
              color: "bg-blue-500",
            },
          ]);
        }
      } catch (e) {
        console.log("JSON parse error:", e);
        console.log("Using fallback for text goal:", financialGoals);
        // Fallback for invalid JSON
        setUserGoals([
          {
            id: 1,
            title: financialGoals,
            target: 50000,
            current: currentSavings,
            deadline: "N/A",
            category: "General",
            icon: Target,
            color: "bg-blue-500",
          },
          ]);
        }
      },
    [setUserGoals, getGoalIcon, getGoalColor] // dependencies
  );  

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await profileAPI.getProfile();
        console.log("Profile API response:", response);
        if (response.success && response.profile) {
          console.log("Setting profile data:", response.profile);
          setProfileData(response.profile);
          parseUserGoals(response.profile.financial_goals, response.profile);
        } else {
          console.log("No profile data or unsuccessful response");
        }
      } catch (error) {
        console.error("Error loading goals:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [parseUserGoals, setProfileData]);


  const calculateProgress = (current, target) => Math.round((current / target) * 100)

  const calculateTimeToGoal = (current, target, monthlyContribution = 5000) => {
    const remaining = target - current
    if (remaining <= 0) return "Goal achieved!"
    const months = Math.ceil(remaining / monthlyContribution)
    return months > 12 ? `${Math.round(months / 12)} years` : `${months} months`
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Financial Goals</h1>
        <div className="flex items-center gap-2 text-gray-500">
          <Target className="h-5 w-5" />
          <span>Track your progress</span>
        </div>
      </div>

      {/* Goals Overview */}
      {loading ? (
        <div className="text-center py-8">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
          <p className="mt-2 text-gray-600">Loading your financial goals...</p>
        </div>
      ) : userGoals.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <Target className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Goals Set Yet</h3>
          <p className="text-gray-600 mb-4">Start by creating a financial goal in your profile.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {userGoals.map((goal) => {
            const progress = calculateProgress(goal.current, goal.target)
            const Icon = goal.icon

            return (
            <div key={goal.id} className="border rounded-lg p-4 shadow-sm bg-white space-y-4">
              {/* Header */}
              <div className="flex items-center justify-between">
                <div className={`p-2 rounded-lg ${goal.color}`}>
                  <Icon className="h-5 w-5 text-white" />
                </div>
                <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100">{goal.category}</span>
              </div>

              <h2 className="text-lg font-semibold">{goal.title}</h2>

              {/* Progress Bar */}
              <div className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Progress</span>
                  <span className="font-medium">{progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded h-2 overflow-hidden">
                  <div
                    className="bg-blue-500 h-2"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>

              {/* Financial Numbers */}
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Current</span>
                  <span className="font-medium">₹{goal.current.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Target</span>
                  <span className="font-medium">₹{goal.target.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Remaining</span>
                  <span className="font-medium text-orange-600">
                    ₹{(goal.target - goal.current).toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Deadline + Time */}
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex items-center gap-1 text-gray-500 text-sm">
                  <Calendar className="h-4 w-4" />
                  <span>{goal.deadline}</span>
                </div>
                <span className="text-sm font-medium text-blue-600">
                  {calculateTimeToGoal(goal.current, goal.target)} to go
                </span>
              </div>
            </div>
            )
          })}
        </div>
      )}

      {/* Asset Allocation */}
      <div className="border rounded-lg p-4 bg-white shadow-sm">
        <h2 className="text-xl font-semibold flex items-center gap-2 mb-4">
          <TrendingUp className="h-5 w-5" />
          Recommended Asset Allocation
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Allocation List */}
          <div className="space-y-4">
            {assetAllocation.map((asset, index) => (
              <div key={index} className="space-y-1">
                <div className="flex justify-between items-center">
                  <span className="font-medium">{asset.category}</span>
                  <span className="text-sm font-semibold">{asset.percentage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded h-2 overflow-hidden">
                  <div
                    className="bg-green-500 h-2"
                    style={{ width: `${asset.percentage}%` }}
                  />
                </div>
                <p className="text-sm text-gray-500">{asset.description}</p>
              </div>
            ))}
          </div>

          {/* Investment Tips */}
          <div className="space-y-3">
            <h3 className="font-semibold text-lg">Investment Tips</h3>
            <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500 text-sm">
              <strong>Start Early:</strong> The power of compounding works best over longer periods.
            </div>
            <div className="p-3 bg-green-50 rounded-lg border-l-4 border-green-500 text-sm">
              <strong>Diversify:</strong> Don't put all your eggs in one basket.
            </div>
            <div className="p-3 bg-orange-50 rounded-lg border-l-4 border-orange-500 text-sm">
              <strong>Review Regularly:</strong> Rebalance your portfolio annually or when life changes.
            </div>
            <div className="p-3 bg-purple-50 rounded-lg border-l-4 border-purple-500 text-sm">
              <strong>Stay Disciplined:</strong> Stick to your plan despite market volatility.
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

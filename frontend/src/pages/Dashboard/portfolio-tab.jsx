import { useState, useEffect } from "react"
import { PieChart, TrendingUp, Target, RefreshCw } from "lucide-react"
import { portfolioAPI } from "../../api/portfolio"

const PortfolioTab = () => {
  const [portfolioData, setPortfolioData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadPortfolioData()
  }, [])

  const loadPortfolioData = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await portfolioAPI.getPortfolioAllocations()
      if (response.success) {
        setPortfolioData(response.data)
      } else {
        setError(response.error)
      }
    } catch (err) {
      setError("Failed to load portfolio data")
    } finally {
      setLoading(false)
    }
  }

  const getColorForAsset = (index) => {
    const colors = [
      'bg-blue-500',
      'bg-green-500', 
      'bg-yellow-500',
      'bg-purple-500',
      'bg-pink-500',
      'bg-indigo-500',
      'bg-red-500',
      'bg-orange-500',
      'bg-teal-500'
    ]
    return colors[index % colors.length]
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading portfolio data...</span>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center lg:text-left">
        <h2 className="text-3xl font-bold text-gray-900 flex items-center">
          <PieChart className="w-8 h-8 mr-3 text-blue-600" />
          <span className="text-blue-600">Portfolio</span>
        </h2>
        {portfolioData?.message && (
          <p className="text-sm text-gray-500 mt-1">{portfolioData.message}</p>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">{error}</div>
            </div>
          </div>
        </div>
      )}

      {portfolioData && (
        <>
          {/* Portfolio Overview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl shadow-md border border-blue-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-blue-700">Risk Level</p>
                  <p className="text-2xl font-bold text-blue-900 mt-1 capitalize">
                    {portfolioData.risk_level || 'Medium'}
                  </p>
                </div>
                <div className="bg-blue-200 p-3 rounded-xl">
                  <Target className="w-6 h-6 text-blue-700" />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl shadow-md border border-green-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-green-700">Total Allocation</p>
                  <p className="text-2xl font-bold text-green-900 mt-1">
                      {portfolioData.total_allocation !== undefined
                        ? Math.min(portfolioData.total_allocation, 100).toFixed(1)
                        : "100"}
                      %
                    </p>
                </div>
                <div className="bg-green-200 p-3 rounded-xl">
                  <PieChart className="w-6 h-6 text-green-700" />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl shadow-md border border-purple-200 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-purple-700">Asset Classes</p>
                  <p className="text-2xl font-bold text-purple-900 mt-1">
                    {Object.keys(portfolioData.allocations || {}).length}
                  </p>
                </div>
                <div className="bg-purple-200 p-3 rounded-xl">
                  <TrendingUp className="w-6 h-6 text-purple-700" />
                </div>
              </div>
            </div>
          </div>

          {/* Asset Allocation */}
          <div className="bg-white rounded-2xl shadow-md border border-gray-100">
            <div className="p-6 border-b border-gray-100">
              <h3 className="text-lg font-semibold text-green-900 bg-green-100 rounded-2xl py-1 px-4 border border-green-300 inline-block">
                Recommended Asset Allocation
              </h3>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {portfolioData.allocations && Object.entries(portfolioData.allocations).map(([asset, percentage], index) => (
                  <div key={asset} className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`w-4 h-4 rounded-full ${getColorForAsset(index)} mr-3`}></div>
                        <span className="font-medium text-gray-900">{asset}</span>
                      </div>
                      <span className="text-lg font-bold text-gray-800">{percentage}%</span>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${getColorForAsset(index)}`} 
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center space-x-4">
            <button 
              onClick={loadPortfolioData}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition flex items-center"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh Recommendations
            </button>
            <button 
              onClick={() => {
                const feedback = { rating: 5, comment: "Looks good!" }
                portfolioAPI.submitPortfolioFeedback(feedback)
                alert("Thank you for your feedback!")
              }}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition flex items-center"
            >
              <Target className="w-4 h-4 mr-2" />
              Accept Recommendations
            </button>
          </div>

          {/* Disclaimer */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">Investment Disclaimer</h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>
                    These are ML-generated recommendations based on your profile. Please consult with a financial advisor 
                    before making investment decisions. Past performance does not guarantee future results.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default PortfolioTab
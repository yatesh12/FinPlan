"use client"

import { useState, useEffect, useCallback } from "react"
import { User, Save, Edit3, Briefcase, Heart, DollarSign, Target } from "lucide-react"
import { profileAPI } from "../../api/profile"

/* --- Enhanced UI primitives --- */
const Card = ({ children, className = "", ...props }) => (
  <div className={`bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-shadow duration-200 ${className}`} {...props}>
    {children}
  </div>
)

const CardHeader = ({ children, className = "", ...props }) => (
  <div className={`p-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white ${className}`} {...props}>
    {children}
  </div>
)

const CardTitle = ({ children, className = "", icon, ...props }) => (
  <div className="flex items-center space-x-3">
    {icon && <div className="p-2 bg-blue-100 rounded-lg">{icon}</div>}
    <h3 className={`text-xl font-bold text-gray-900 ${className}`} {...props}>
      {children}
    </h3>
  </div>
)

const CardContent = ({ children, className = "", ...props }) => (
  <div className={`p-6 ${className}`} {...props}>
    {children}
  </div>
)

const Button = ({ children, onClick, disabled = false, className = "", type = "button", ...props }) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center rounded-md transition-colors focus:outline-none ${
        disabled ? "opacity-60 cursor-not-allowed" : ""
      } ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}

const Label = ({ htmlFor, children, className = "" }) => (
  <label htmlFor={htmlFor} className={`block text-sm font-medium ${className}`}>
    {children}
  </label>
)

const TextInput = ({ id, type = "text", value, onChange, disabled = false, className = "", ...props }) => (
  <input
    id={id}
    type={type}
    value={value}
    onChange={onChange}
    disabled={disabled}
    className={`w-full p-2 border border-input rounded-md bg-background ${className}`}
    {...props}
  />
)

/* ---------------- Component ---------------- */
const ProfileTab = ({ userData = {} }) => {
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [profileData, setProfileData] = useState(null)
  const [formData, setFormData] = useState({
    full_name: userData?.full_name || "",
    date_of_birth: userData?.date_of_birth || "",
    gender: userData?.gender || "",
    occupation_type: userData?.occupation_type || "",
    marital_status: userData?.marital_status || "",
    number_of_dependents: userData?.number_of_dependents || 0,
    monthly_income: userData?.monthly_income || 0,
    monthly_expenses: userData?.monthly_expenses || 0,
    monthly_savings: userData?.monthly_savings || 0,
    has_loans: userData?.has_loans || false,
    loan_type: userData?.loan_type || "",
    monthly_emi: userData?.monthly_emi || 0,
    primary_goal: userData?.primary_goal || "",
    goal_target_amount: userData?.goal_target_amount || 0,
    goal_timeline_years: userData?.goal_timeline_years || 0,
    preferred_investment: userData?.preferred_investment || "",
    investment_horizon: userData?.investment_horizon || "",
    risk_comfort_level: userData?.risk_comfort_level || "",
    health_insurance_cover: userData?.health_insurance_cover || 0,
    life_insurance_cover: userData?.life_insurance_cover || 0,
    emergency_fund_amount: userData?.emergency_fund_amount || 0,
  })

  const loadProfile = useCallback(async () => {
  try {
    console.log("Loading profile...");
    const response = await profileAPI.getProfile();
    console.log("Profile API response:", response);

    if (response?.success && response?.profile) {
      const profile = response.profile;
      console.log("Profile data found:", profile);

      setProfileData(profile);

      // Safely update form data based on API response
      setFormData((prevFormData) => {
        const updatedFormData = {
          ...prevFormData,
          monthly_income: profile.income ?? 0,
          monthly_expenses: profile.expenses ?? 0,
          monthly_savings: profile.savings ?? 0,
          risk_comfort_level: profile.risk_tolerance ?? "",
          primary_goal: profile.financial_goals ?? "",
          // If age exists, estimate date_of_birth
          date_of_birth: profile.age
            ? new Date(
                new Date().getFullYear() - profile.age,
                0,
                1
              )
                .toISOString()
                .split("T")[0]
            : "",
          investment_horizon: profile.investment_experience ?? "",
        };

        console.log("Updated form data:", updatedFormData);
        return updatedFormData;
      });
    } else {
      console.log("No profile data found or API call failed");
    }
  } catch (error) {
    console.error("Error loading profile:", error);
  }
}, []); // dependencies go here


  // Load profile data on component mount
  useEffect(() => {
    loadProfile()
  }, [loadProfile])

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      const response = await profileAPI.updateProfile(formData)
      if (response.success) {
        console.log("Profile saved successfully")
        setIsEditing(false)
        // Reload profile data to show updated values
        loadProfile()
      } else {
        console.error("Failed to save profile:", response.error)
        alert("Failed to save profile. Please try again.")
      }
    } catch (error) {
      console.error("Error saving profile:", error)
      alert("Error saving profile. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Enhanced Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 border border-blue-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-white p-4 rounded-full shadow-md">
              <User className="w-8 h-8 text-blue-600" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900">Profile Management</h2>
              <p className="text-gray-600 mt-1">Keep your financial information up to date</p>
              {profileData && (
                <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                  <span>Last updated: {new Date(profileData.updated_at).toLocaleDateString()}</span>
                  <span className="flex items-center">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                    Profile Complete
                  </span>
                </div>
              )}
            </div>
          </div>
          <Button 
            onClick={() => (isEditing ? handleSave() : setIsEditing(true))} 
            disabled={loading}
            className={`flex items-center px-6 py-3 rounded-lg font-medium transition-all ${
              isEditing 
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-lg' 
                : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl'
            }`}
          >
            {loading ? (
              <>
                <div className="w-4 h-4 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Saving...
              </>
            ) : isEditing ? (
              <>
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </>
            ) : (
              <>
                <Edit3 className="w-4 h-4 mr-2" />
                Edit Profile
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Personal Information */}
      <Card>
        <CardHeader>
          <CardTitle icon={<User className="w-5 h-5 text-blue-600" />}>
            Personal Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="full_name" className="text-muted-foreground">
                Full Name
              </Label>
              <TextInput
                id="full_name"
                value={formData.full_name}
                onChange={(e) => handleInputChange("full_name", e.target.value)}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="date_of_birth" className="text-muted-foreground">
                Date of Birth
              </Label>
              <TextInput
                id="date_of_birth"
                type="date"
                value={formData.date_of_birth}
                onChange={(e) => handleInputChange("date_of_birth", e.target.value)}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="gender" className="text-muted-foreground">
                Gender
              </Label>
              <select
                id="gender"
                value={formData.gender}
                onChange={(e) => handleInputChange("gender", e.target.value)}
                disabled={!isEditing}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <Label htmlFor="marital_status" className="text-muted-foreground">
                Marital Status
              </Label>
              <select
                id="marital_status"
                value={formData.marital_status}
                onChange={(e) => handleInputChange("marital_status", e.target.value)}
                disabled={!isEditing}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="">Select Status</option>
                <option value="single">Single</option>
                <option value="married">Married</option>
                <option value="married_with_children">Married with Children</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Professional Information */}
      <Card>
        <CardHeader>
          <CardTitle icon={<Briefcase className="w-5 h-5 text-blue-600" />}>
            Professional Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="occupation_type" className="text-muted-foreground">
                Occupation Type
              </Label>
              <select
                id="occupation_type"
                value={formData.occupation_type}
                onChange={(e) => handleInputChange("occupation_type", e.target.value)}
                disabled={!isEditing}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="">Select Occupation</option>
                <option value="salaried_private">Salaried Private</option>
                <option value="salaried_govt">Salaried Government</option>
                <option value="self_employed">Self Employed</option>
                <option value="business">Business</option>
                <option value="student">Student</option>
                <option value="retired">Retired</option>
              </select>
            </div>
            <div>
              <Label htmlFor="number_of_dependents" className="text-muted-foreground">
                Number of Dependents
              </Label>
              <TextInput
                id="number_of_dependents"
                type="number"
                value={formData.number_of_dependents}
                onChange={(e) =>
                  handleInputChange("number_of_dependents", Number.isNaN(parseInt(e.target.value, 10)) ? 0 : parseInt(e.target.value, 10))
                }
                disabled={!isEditing}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Financial Information */}
      <Card>
        <CardHeader>
          <CardTitle icon={<DollarSign className="w-5 h-5 text-green-600" />}>
            Financial Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="monthly_income" className="text-muted-foreground">
                Monthly Income
              </Label>
              <TextInput
                id="monthly_income"
                type="number"
                value={formData.monthly_income}
                onChange={(e) => handleInputChange("monthly_income", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="monthly_expenses" className="text-muted-foreground">
                Monthly Expenses
              </Label>
              <TextInput
                id="monthly_expenses"
                type="number"
                value={formData.monthly_expenses}
                onChange={(e) => handleInputChange("monthly_expenses", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="monthly_savings" className="text-muted-foreground">
                Monthly Savings
              </Label>
              <TextInput
                id="monthly_savings"
                type="number"
                value={formData.monthly_savings}
                onChange={(e) => handleInputChange("monthly_savings", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="has_loans" className="text-muted-foreground">
                Has Loans
              </Label>
              <select
                id="has_loans"
                value={formData.has_loans.toString()}
                onChange={(e) => handleInputChange("has_loans", e.target.value === "true")}
                disabled={!isEditing}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="false">No</option>
                <option value="true">Yes</option>
              </select>
            </div>
            {formData.has_loans && (
              <>
                <div>
                  <Label htmlFor="loan_type" className="text-muted-foreground">
                    Loan Type
                  </Label>
                  <select
                    id="loan_type"
                    value={formData.loan_type}
                    onChange={(e) => handleInputChange("loan_type", e.target.value)}
                    disabled={!isEditing}
                    className="w-full p-2 border border-input rounded-md bg-background"
                  >
                    <option value="">Select Loan Type</option>
                    <option value="home">Home Loan</option>
                    <option value="car">Car Loan</option>
                    <option value="education">Education Loan</option>
                    <option value="personal">Personal Loan</option>
                    <option value="business">Business Loan</option>
                  </select>
                </div>
                <div>
                  <Label htmlFor="monthly_emi" className="text-muted-foreground">
                    Monthly EMI
                  </Label>
                  <TextInput
                    id="monthly_emi"
                    type="number"
                    value={formData.monthly_emi}
                    onChange={(e) => handleInputChange("monthly_emi", Number.parseFloat(e.target.value))}
                    disabled={!isEditing}
                  />
                </div>
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Investment Goals */}
      <Card>
        <CardHeader>
          <CardTitle icon={<Target className="w-5 h-5 text-purple-600" />}>
            Investment Goals & Preferences
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="primary_goal" className="text-muted-foreground">
                Primary Goal
              </Label>
              <select
                id="primary_goal"
                value={formData.primary_goal}
                onChange={(e) => handleInputChange("primary_goal", e.target.value)}
                disabled={!isEditing}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="">Select Goal</option>
                <option value="retirement">Retirement</option>
                <option value="child_education">Child Education</option>
                <option value="buying_home">Buying Home</option>
                <option value="emergency_fund">Emergency Fund</option>
                <option value="wealth_creation">Wealth Creation</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <Label htmlFor="goal_target_amount" className="text-muted-foreground">
                Goal Target Amount
              </Label>
              <TextInput
                id="goal_target_amount"
                type="number"
                value={formData.goal_target_amount}
                onChange={(e) => handleInputChange("goal_target_amount", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="goal_timeline_years" className="text-muted-foreground">
                Goal Timeline (Years)
              </Label>
              <TextInput
                id="goal_timeline_years"
                type="number"
                value={formData.goal_timeline_years}
                onChange={(e) => handleInputChange("goal_timeline_years", Number.parseInt(e.target.value))}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="risk_comfort_level" className="text-muted-foreground">
                Risk Comfort Level
              </Label>
              <select
                id="risk_comfort_level"
                value={formData.risk_comfort_level}
                onChange={(e) => handleInputChange("risk_comfort_level", e.target.value)}
                disabled={!isEditing}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="">Select Risk Level</option>
                <option value="low">Low</option>
                <option value="moderate">Moderate</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Insurance & Emergency Fund */}
      <Card>
        <CardHeader>
          <CardTitle icon={<Heart className="w-5 h-5 text-red-500" />}>
            Insurance & Emergency Fund
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="health_insurance_cover" className="text-muted-foreground">
                Health Insurance Cover
              </Label>
              <TextInput
                id="health_insurance_cover"
                type="number"
                value={formData.health_insurance_cover}
                onChange={(e) => handleInputChange("health_insurance_cover", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="life_insurance_cover" className="text-muted-foreground">
                Life Insurance Cover
              </Label>
              <TextInput
                id="life_insurance_cover"
                type="number"
                value={formData.life_insurance_cover}
                onChange={(e) => handleInputChange("life_insurance_cover", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
            <div>
              <Label htmlFor="emergency_fund_amount" className="text-muted-foreground">
                Emergency Fund Amount
              </Label>
              <TextInput
                id="emergency_fund_amount"
                type="number"
                value={formData.emergency_fund_amount}
                onChange={(e) => handleInputChange("emergency_fund_amount", Number.parseFloat(e.target.value))}
                disabled={!isEditing}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default ProfileTab

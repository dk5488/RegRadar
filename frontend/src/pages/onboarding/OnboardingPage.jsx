import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { BUSINESS_TYPES, INDUSTRY_SECTORS, INDIAN_STATES } from '../../utils/constants';
import './Onboarding.css';

export function OnboardingPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 3;

  const [formData, setFormData] = useState({
    companyName: user?.name || '',
    businessType: '',
    industry: '',
    registrationNumber: '',
    state: '',
    employeeCount: '',
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleNext = () => {
    if (currentStep < totalSteps) setCurrentStep(currentStep + 1);
  };

  const handlePrev = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Simulate API Call for onboarding
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log('Onboarding complete:', formData);
      // Navigate to the Dashboard/Alerts Inbox
      navigate('/alerts');
    } catch (error) {
      console.error('Onboarding failed', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="onboarding-container">
      {/* Background Shapes for Premium Feel */}
      <div className="onboarding-bg-shape onboarding-shape-1" />
      <div className="onboarding-bg-shape onboarding-shape-2" />

      <div className="onboarding-card">
        {/* Progress Stepper */}
        <div className="stepper">
          <div 
            className="stepper-progress" 
            style={{ width: `${((currentStep - 1) / (totalSteps - 1)) * 100}%` }} 
          />
          {[1, 2, 3].map((step) => (
            <div 
              key={step} 
              className={`step-indicator ${currentStep === step ? 'active' : ''} ${currentStep > step ? 'completed' : ''}`}
            >
              {currentStep > step ? '✓' : step}
            </div>
          ))}
        </div>

        <form onSubmit={currentStep === totalSteps ? handleSubmit : (e) => e.preventDefault()}>
          
          {/* ── Step 1: Basic Info ─────────────────────────────────────── */}
          {currentStep === 1 && (
            <div className="step-content">
              <div className="step-header">
                <h1 className="step-title">Welcome to RegRadar</h1>
                <p className="step-subtitle">Let's set up your compliance profile. What is your company's name?</p>
              </div>

              <div className="onboarding-form">
                <div className="form-group">
                  <label className="form-label" htmlFor="companyName">Company Name</label>
                  <input
                    id="companyName"
                    name="companyName"
                    type="text"
                    className="form-input"
                    value={formData.companyName}
                    onChange={handleChange}
                    placeholder="Acme Corporation"
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label" htmlFor="registrationNumber">CIN / Registration Number (Optional)</label>
                  <input
                    id="registrationNumber"
                    name="registrationNumber"
                    type="text"
                    className="form-input"
                    value={formData.registrationNumber}
                    onChange={handleChange}
                    placeholder="L12345MH2000PLC123456"
                  />
                </div>
              </div>
            </div>
          )}

          {/* ── Step 2: Industry & Type ────────────────────────────────── */}
          {currentStep === 2 && (
            <div className="step-content">
              <div className="step-header">
                <h1 className="step-title">Business Profile</h1>
                <p className="step-subtitle">This helps us fetch the right regulations for you.</p>
              </div>

              <div className="onboarding-form">
                <div className="form-group">
                  <label className="form-label" htmlFor="businessType">Business Entity Type</label>
                  <select
                    id="businessType"
                    name="businessType"
                    className="form-select"
                    value={formData.businessType}
                    onChange={handleChange}
                    required
                  >
                    <option value="" disabled>Select business type</option>
                    {BUSINESS_TYPES.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label" htmlFor="industry">Industry Sector</label>
                  <select
                    id="industry"
                    name="industry"
                    className="form-select"
                    value={formData.industry}
                    onChange={handleChange}
                    required
                  >
                    <option value="" disabled>Select your industry</option>
                    {INDUSTRY_SECTORS.map(sector => (
                      <option key={sector} value={sector}>{sector}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* ── Step 3: Location & Size ────────────────────────────────── */}
          {currentStep === 3 && (
            <div className="step-content">
              <div className="step-header">
                <h1 className="step-title">Operations</h1>
                <p className="step-subtitle">Where are you located and how big is your team?</p>
              </div>

              <div className="onboarding-form">
                <div className="form-group">
                  <label className="form-label" htmlFor="state">Primary State of Operation</label>
                  <select
                    id="state"
                    name="state"
                    className="form-select"
                    value={formData.state}
                    onChange={handleChange}
                    required
                  >
                    <option value="" disabled>Select state</option>
                    {INDIAN_STATES.map(state => (
                      <option key={state} value={state}>{state}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Employee Count</label>
                  <div className="radio-card-group">
                    {['1-10', '11-50', '51-200', '201+'].map(size => (
                      <label 
                        key={size} 
                        className={`radio-card ${formData.employeeCount === size ? 'active' : ''}`}
                      >
                        <input
                          type="radio"
                          name="employeeCount"
                          value={size}
                          checked={formData.employeeCount === size}
                          onChange={handleChange}
                          className="radio-card-input"
                          required
                        />
                        <div className="radio-card-content">
                          <span className="radio-card-title">{size} Employees</span>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ── Action Buttons ─────────────────────────────────────────── */}
          <div className="step-actions">
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={handlePrev} 
              disabled={currentStep === 1 || isLoading}
            >
              Back
            </button>
            
            {currentStep < totalSteps ? (
              <button 
                type="button" 
                className="btn btn-primary" 
                onClick={handleNext}
                disabled={
                  (currentStep === 1 && !formData.companyName) ||
                  (currentStep === 2 && (!formData.businessType || !formData.industry))
                }
              >
                Continue
              </button>
            ) : (
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={isLoading || !formData.state || !formData.employeeCount}
              >
                {isLoading ? 'Setting up...' : 'Complete Setup'}
              </button>
            )}
          </div>

        </form>
      </div>
    </div>
  );
}

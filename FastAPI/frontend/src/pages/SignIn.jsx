import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './SignIn.css';

const API_BASE_URL = 'http://localhost:8000'; // Change this to your FastAPI backend URL

function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Sign in failed');
      }

      // Store token in localStorage
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      // Redirect to account settings or home
      navigate('/account-settings');
    } catch (err) {
      setError(err.message || 'Failed to sign in. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signin-page">
      <div className="signin-container">
        <div className="signin-card">
          <h1 className="signin-title">Apple Store India</h1>
          <h2 className="signin-heading">Sign in to Apple Store</h2>
          <p className="signin-subtitle">Enter your email and password to continue.</p>

          {error && <div className="error-message">{error}</div>}

          <form className="signin-form" onSubmit={handleSignIn}>
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                placeholder="*******"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
              <Link to="/forgot-password" className="forgot-password">Forgot?</Link>
            </div>

            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="demo-accounts">
            <h3>Demo Accounts (Ready to test):</h3>
            <div className="demo-account">
              <span className="demo-label">Customer:</span>
              <span className="demo-credentials">manoj@gmail.com / manoj123</span>
            </div>
            <div className="demo-account">
              <span className="demo-label">Admin:</span>
              <span className="demo-credentials">admin@applestore.in / admin123</span>
            </div>
          </div>

          <div className="signup-link">
            <p>Don't have an Apple account? <Link to="/create-account">Create yours now →</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignIn;

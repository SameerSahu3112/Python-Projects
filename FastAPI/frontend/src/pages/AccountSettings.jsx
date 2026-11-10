import { Link } from 'react-router-dom';
import { useState } from 'react';
import './AccountSettings.css';

function AccountSettings() {
  const [personalInfo, setPersonalInfo] = useState({
    fullName: 'Manoj Sahu',
    email: 'manoj@gmail.com',
    phone: '+91 98765 43210'
  });

  const handleChange = (e) => {
    setPersonalInfo({
      ...personalInfo,
      [e.target.name]: e.target.value
    });
  };

  const handleSaveProfile = (e) => {
    e.preventDefault();
    // TODO: Implement save profile logic with backend
    console.log('Save profile:', personalInfo);
  };

  const handleDeleteAddress = () => {
    // TODO: Implement delete address logic with backend
    console.log('Delete address');
  };

  return (
    <div className="account-settings-page">
      <div className="section">
        <div className="page-header">
          <h1 className="page-title">Account Settings</h1>
          <p className="page-subtitle">Manage your personal information, saved addresses, and preferences.</p>
        </div>

        <div className="settings-grid">
          <div className="settings-card">
            <h2 className="card-title">Personal Information</h2>
            <form className="settings-form" onSubmit={handleSaveProfile}>
              <div className="form-group">
                <label htmlFor="fullName">Full Name</label>
                <input
                  type="text"
                  id="fullName"
                  name="fullName"
                  value={personalInfo.fullName}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={personalInfo.email}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={personalInfo.phone}
                  onChange={handleChange}
                />
              </div>

              <button type="submit" className="btn btn-primary">Save Profile Changes</button>
            </form>
          </div>

          <div className="settings-card">
            <h2 className="card-title">Saved Addresses</h2>
            <div className="address-item">
              <div className="address-content">
                <p className="address-name">Manoj Sahu</p>
                <p className="address-text">123 Tech Street, Bangalore, Karnataka 560001</p>
                <p className="address-phone">+91 98765 43210</p>
              </div>
              <div className="address-actions">
                <button className="btn btn-secondary btn-sm">Edit</button>
                <button className="btn btn-outline btn-sm" onClick={handleDeleteAddress}>Delete</button>
              </div>
            </div>
            <button className="btn btn-secondary btn-full">Add New Address</button>
          </div>

          <div className="settings-card">
            <h2 className="card-title">Quick Actions</h2>
            <div className="quick-actions">
              <Link to="/my-orders" className="quick-action-link">
                <span className="action-icon">📦</span>
                <span>Order History</span>
              </Link>
              <Link to="/my-wishlist" className="quick-action-link">
                <span className="action-icon">❤️</span>
                <span>Wishlist</span>
              </Link>
              <Link to="/signin" className="quick-action-link">
                <span className="action-icon">🚪</span>
                <span>Sign Out</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AccountSettings;

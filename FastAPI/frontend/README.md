# Apple Store Frontend

A modern Apple Store-inspired e-commerce frontend built with React and Vite.

## Features

- **Sign In Page** - User authentication with demo accounts
- **Create Account Page** - User registration form
- **Account Settings** - Manage personal information, addresses, and preferences
- **My Orders** - View and track order history
- **My Wishlist** - Save and manage favorite items
- **Order Confirmation** - Detailed order summary after purchase

## Tech Stack

- React 18
- Vite
- React Router DOM
- Lucide React (Icons)

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Header.css
│   │   ├── Footer.jsx
│   │   └── Footer.css
│   ├── pages/
│   │   ├── SignIn.jsx
│   │   ├── SignIn.css
│   │   ├── CreateAccount.jsx
│   │   ├── CreateAccount.css
│   │   ├── AccountSettings.jsx
│   │   ├── AccountSettings.css
│   │   ├── MyOrders.jsx
│   │   ├── MyOrders.css
│   │   ├── MyWishlist.jsx
│   │   ├── MyWishlist.css
│   │   ├── OrderConfirmation.jsx
│   │   └── OrderConfirmation.css
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── package.json
└── vite.config.js
```

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

## Available Routes

- `/` - Sign In page (default)
- `/signin` - Sign In page
- `/create-account` - Create Account page
- `/account-settings` - Account Settings page
- `/my-orders` - My Orders page
- `/my-wishlist` - My Wishlist page
- `/order-confirmation` - Order Confirmation page

## Demo Accounts

The Sign In page includes demo accounts for testing:

- **Customer**: manoj@gmail.com / manoj123
- **Admin**: admin@applestore.in / admin123

## Backend Integration

This frontend is designed to work with a FastAPI backend. To integrate with your backend:

1. Update the form submission handlers in each page to make API calls
2. Replace static data with API responses
3. Add authentication state management
4. Implement error handling

Example API integration pattern:

```javascript
const handleSignIn = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('http://localhost:8000/api/signin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    // Handle success/error
  } catch (error) {
    console.error('Sign in error:', error);
  }
};
```

## Styling

The application uses a clean, modern design inspired by Apple's design language:
- Minimalist color palette (whites, grays, and accent blues)
- Rounded corners and subtle shadows
- Responsive grid layouts
- Smooth transitions and hover effects

## Future Enhancements

- Product listing and detail pages
- Shopping cart functionality
- Search functionality
- User authentication state management
- Real-time order tracking
- Payment integration

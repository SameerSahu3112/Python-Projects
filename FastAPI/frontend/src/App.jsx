import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import SignIn from './pages/SignIn';
import CreateAccount from './pages/CreateAccount';
import AccountSettings from './pages/AccountSettings';
import MyOrders from './pages/MyOrders';
import MyWishlist from './pages/MyWishlist';
import OrderConfirmation from './pages/OrderConfirmation';
import './App.css';
import './components/Header.css';
import './components/Footer.css';
import './pages/SignIn.css';
import './pages/CreateAccount.css';
import './pages/AccountSettings.css';
import './pages/MyOrders.css';
import './pages/MyWishlist.css';
import './pages/OrderConfirmation.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<SignIn />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/create-account" element={<CreateAccount />} />
            <Route path="/account-settings" element={<AccountSettings />} />
            <Route path="/my-orders" element={<MyOrders />} />
            <Route path="/my-wishlist" element={<MyWishlist />} />
            <Route path="/order-confirmation" element={<OrderConfirmation />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;

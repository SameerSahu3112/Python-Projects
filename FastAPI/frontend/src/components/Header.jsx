import { Link } from 'react-router-dom';
import { Search, Heart, ShoppingBag } from 'lucide-react';

function Header() {
  return (
    <header className="header">
      <nav className="nav">
        <div className="nav-container">
          <div className="nav-left">
            <Link to="/" className="nav-logo">Apple</Link>
            <div className="nav-links">
              <Link to="/store">Store</Link>
              <Link to="/mac">Mac</Link>
              <Link to="/ipad">iPad</Link>
              <Link to="/iphone">iPhone</Link>
              <Link to="/watch">Watch</Link>
              <Link to="/airpods">AirPods</Link>
              <Link to="/accessories">Accessories</Link>
              <Link to="/account-settings">Account</Link>
            </div>
          </div>
          <div className="nav-right">
            <button className="nav-icon"><Search size={18} /></button>
            <button className="nav-icon"><Heart size={18} /></button>
            <button className="nav-icon"><ShoppingBag size={18} /></button>
          </div>
        </div>
      </nav>
      <div className="promo-banner">
        Make something wonderful. Use APPLE10 for 10% off your next favourite.
      </div>
    </header>
  );
}

export default Header;

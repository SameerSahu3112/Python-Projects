import { Link } from 'react-router-dom';
import { CheckCircle } from 'lucide-react';
import './OrderConfirmation.css';

function OrderConfirmation() {
  const orderDetails = {
    orderNumber: 'AS-IN-10482',
    orderDate: 'Nov 10, 2025',
    paymentMethod: 'Credit Card ending in 4242',
    totalAmount: '₹1,64,900',
    status: 'Processing',
    estimatedDelivery: 'Nov 15 - Nov 18, 2025',
    items: [
      {
        name: 'iPhone 16 Pro',
        description: '256GB, Desert Titanium',
        price: '₹1,44,900',
        quantity: 1
      },
      {
        name: 'AirPods Pro',
        description: 'USB-C, Noise Cancellation',
        price: '₹20,000',
        quantity: 1
      }
    ],
    shippingAddress: {
      name: 'Manoj Sahu',
      address: '123 Tech Street, Bangalore, Karnataka 560001',
      phone: '+91 98765 43210'
    },
    summary: {
      subtotal: '₹1,64,900',
      gst: '₹29,682',
      shipping: 'Free',
      total: '₹1,94,582'
    }
  };

  return (
    <div className="order-confirmation-page">
      <div className="section">
        <div className="confirmation-header">
          <div className="success-icon">
            <CheckCircle size={64} color="#34c759" />
          </div>
          <h1 className="confirmation-title">Thank you for your order!</h1>
          <p className="confirmation-subtitle">Your order has been placed and is now being processed.</p>
          <button className="order-number-btn">{orderDetails.orderNumber}</button>
        </div>

        <div className="confirmation-grid">
          <div className="confirmation-card">
            <h2 className="card-title">Order Summary</h2>
            <div className="summary-row">
              <span className="summary-label">Order Date</span>
              <span className="summary-value">{orderDetails.orderDate}</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Payment Method</span>
              <span className="summary-value">{orderDetails.paymentMethod}</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Total Amount Paid</span>
              <span className="summary-value">{orderDetails.totalAmount}</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Status</span>
              <span className={`status status-${orderDetails.status.toLowerCase()}`}>{orderDetails.status}</span>
            </div>
          </div>

          <div className="confirmation-card">
            <h2 className="card-title">Items in this Order</h2>
            <div className="order-items">
              {orderDetails.items.map((item, index) => (
                <div key={index} className="order-item">
                  <div className="item-details">
                    <h3 className="item-name">{item.name}</h3>
                    <p className="item-description">{item.description}</p>
                    <p className="item-price">{item.price}</p>
                    <p className="item-quantity">Qty: {item.quantity}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="confirmation-card">
            <h2 className="card-title">Delivering To</h2>
            <div className="shipping-address">
              <p className="address-name">{orderDetails.shippingAddress.name}</p>
              <p className="address-text">{orderDetails.shippingAddress.address}</p>
              <p className="address-phone">{orderDetails.shippingAddress.phone}</p>
              <div className="estimated-delivery">
                <span className="delivery-label">Estimated Delivery:</span>
                <span className="delivery-date">{orderDetails.estimatedDelivery}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="financial-summary">
          <div className="summary-row">
            <span className="summary-label">Subtotal</span>
            <span className="summary-value">{orderDetails.summary.subtotal}</span>
          </div>
          <div className="summary-row">
            <span className="summary-label">GST (18%)</span>
            <span className="summary-value">{orderDetails.summary.gst}</span>
          </div>
          <div className="summary-row">
            <span className="summary-label">Shipping</span>
            <span className="summary-value">{orderDetails.summary.shipping}</span>
          </div>
          <div className="summary-row total-row">
            <span className="summary-label total-label">Grand Total</span>
            <span className="summary-value total-value">{orderDetails.summary.total}</span>
          </div>
        </div>

        <div className="action-buttons">
          <Link to="/my-orders" className="btn btn-primary">View My Orders</Link>
          <Link to="/" className="btn btn-secondary">Continue Shopping</Link>
        </div>
      </div>
    </div>
  );
}

export default OrderConfirmation;

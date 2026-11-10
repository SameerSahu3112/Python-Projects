import { useState } from 'react';
import './MyOrders.css';

function MyOrders() {
  const [activeTab, setActiveTab] = useState('all');

  const orders = [
    {
      id: 'AS-IN-10482',
      date: 'Nov 10, 2025',
      payment: 'Credit Card ending in 4242',
      total: '₹1,64,900',
      status: 'Processing',
      items: [
        {
          name: 'iPhone 16 Pro',
          description: '256GB, Desert Titanium',
          price: '₹1,44,900',
          quantity: 1,
          image: '📱'
        },
        {
          name: 'AirPods Pro',
          description: 'USB-C, Noise Cancellation',
          price: '₹20,000',
          quantity: 1,
          image: '🎧'
        }
      ]
    }
  ];

  return (
    <div className="my-orders-page">
      <div className="section">
        <div className="page-header">
          <h1 className="page-title">My Orders</h1>
          <p className="page-subtitle">Track, review, and manage your recent Apple purchases.</p>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All orders
          </button>
          <button
            className={`tab ${activeTab === 'in-progress' ? 'active' : ''}`}
            onClick={() => setActiveTab('in-progress')}
          >
            In progress
          </button>
        </div>

        <div className="orders-list">
          {orders.map((order) => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <div className="order-info">
                  <p className="order-number">Order Number: {order.id}</p>
                  <p className="order-date">Date Placed: {order.date}</p>
                  <p className="order-payment">Payment: {order.payment}</p>
                </div>
                <div className="order-total">
                  <p className="total-amount">{order.total}</p>
                  <span className={`status status-${order.status.toLowerCase()}`}>{order.status}</span>
                </div>
              </div>

              <div className="order-items">
                {order.items.map((item, index) => (
                  <div key={index} className="order-item">
                    <div className="item-image">{item.image}</div>
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
          ))}
        </div>

        <div className="support-section">
          <h2 className="support-title">A little help goes a long way.</h2>
          <p className="support-text">Need assistance with your order? Our support team is here to help.</p>
          <button className="btn btn-primary">Contact Support</button>
        </div>
      </div>
    </div>
  );
}

export default MyOrders;

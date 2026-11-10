import './MyWishlist.css';

function MyWishlist() {
  const wishlistItems = [
    {
      id: 1,
      name: 'MacBook Air',
      description: '13-inch, M3 chip, 8GB RAM, 256GB SSD',
      price: '₹99,900',
      image: '💻'
    },
    {
      id: 2,
      name: 'iPad Air',
      description: '11-inch, M2 chip, Wi-Fi, 64GB',
      price: '₹59,900',
      image: '📱'
    },
    {
      id: 3,
      name: 'AirPods Pro',
      description: 'USB-C, Noise Cancellation, MagSafe',
      price: '₹20,000',
      image: '🎧'
    }
  ];

  const handleAddToBag = (itemId) => {
    // TODO: Implement add to bag logic with backend
    console.log('Add to bag:', itemId);
  };

  const handleRemoveFromWishlist = (itemId) => {
    // TODO: Implement remove from wishlist logic with backend
    console.log('Remove from wishlist:', itemId);
  };

  return (
    <div className="wishlist-page">
      <div className="section">
        <div className="page-header">
          <h1 className="page-title">My Wishlist</h1>
          <p className="page-subtitle">Save items you love so you can easily find them later.</p>
        </div>

        <div className="wishlist-grid">
          {wishlistItems.map((item) => (
            <div key={item.id} className="wishlist-card">
              <div className="card-badge">SAVED FOR LATER</div>
              <div className="card-image">{item.image}</div>
              <div className="card-content">
                <h3 className="card-title">{item.name}</h3>
                <p className="card-description">{item.description}</p>
                <p className="card-price">{item.price}</p>
                <div className="card-actions">
                  <button className="btn btn-primary btn-full" onClick={() => handleAddToBag(item.id)}>
                    Add to Bag
                  </button>
                  <button className="btn btn-outline btn-full" onClick={() => handleRemoveFromWishlist(item.id)}>
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="explore-section">
          <h2 className="explore-title">Find your next favourite</h2>
          <p className="explore-text">Explore Products</p>
        </div>
      </div>
    </div>
  );
}

export default MyWishlist;

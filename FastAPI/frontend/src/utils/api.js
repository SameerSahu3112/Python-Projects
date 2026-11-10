// API utility functions for communicating with FastAPI backend

const API_BASE_URL = 'http://localhost:8000'; // Change this to your FastAPI backend URL

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('token');
};

// Helper function to make authenticated requests
const authFetch = async (url, options = {}) => {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return fetch(url, { ...options, headers });
};

// Auth API
export const authAPI = {
  signIn: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/api/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return response.json();
  },

  createAccount: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/api/create-account`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return response.json();
  },

  signOut: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

// User API
export const userAPI = {
  getProfile: async () => {
    const response = await authFetch(`${API_BASE_URL}/api/user/profile`);
    return response.json();
  },

  updateProfile: async (userData) => {
    const response = await authFetch(`${API_BASE_URL}/api/user/profile`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
    return response.json();
  },

  getAddresses: async () => {
    const response = await authFetch(`${API_BASE_URL}/api/user/addresses`);
    return response.json();
  },

  addAddress: async (addressData) => {
    const response = await authFetch(`${API_BASE_URL}/api/user/addresses`, {
      method: 'POST',
      body: JSON.stringify(addressData),
    });
    return response.json();
  },

  deleteAddress: async (addressId) => {
    const response = await authFetch(`${API_BASE_URL}/api/user/addresses/${addressId}`, {
      method: 'DELETE',
    });
    return response.json();
  },
};

// Orders API
export const ordersAPI = {
  getOrders: async () => {
    const response = await authFetch(`${API_BASE_URL}/api/orders`);
    return response.json();
  },

  getOrderById: async (orderId) => {
    const response = await authFetch(`${API_BASE_URL}/api/orders/${orderId}`);
    return response.json();
  },

  createOrder: async (orderData) => {
    const response = await authFetch(`${API_BASE_URL}/api/orders`, {
      method: 'POST',
      body: JSON.stringify(orderData),
    });
    return response.json();
  },
};

// Wishlist API
export const wishlistAPI = {
  getWishlist: async () => {
    const response = await authFetch(`${API_BASE_URL}/api/wishlist`);
    return response.json();
  },

  addToWishlist: async (productId) => {
    const response = await authFetch(`${API_BASE_URL}/api/wishlist`, {
      method: 'POST',
      body: JSON.stringify({ product_id: productId }),
    });
    return response.json();
  },

  removeFromWishlist: async (itemId) => {
    const response = await authFetch(`${API_BASE_URL}/api/wishlist/${itemId}`, {
      method: 'DELETE',
    });
    return response.json();
  },
};

export default API_BASE_URL;

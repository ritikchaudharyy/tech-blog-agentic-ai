export const auth = {
  isAuthenticated: false,
  role: null, // 'user' | 'admin'
  apiKey: null,

  initialize() {
    const storedAuth = localStorage.getItem('auth_session');
    if (storedAuth) {
      const { role, apiKey } = JSON.parse(storedAuth);
      this.isAuthenticated = true;
      this.role = role;
      this.apiKey = apiKey || null;
    }
  },

  login(email, apiKey = null) {
    this.isAuthenticated = true;
    this.role = email === 'admin@example.com' ? 'admin' : 'user';
    this.apiKey = apiKey;

    localStorage.setItem(
      'auth_session',
      JSON.stringify({
        isAuthenticated: true,
        role: this.role,
        apiKey: this.apiKey,
      })
    );
  },

  logout() {
    this.isAuthenticated = false;
    this.role = null;
    this.apiKey = null;
    localStorage.removeItem('auth_session');
  },
};

// Auto-initialize on load
auth.initialize();

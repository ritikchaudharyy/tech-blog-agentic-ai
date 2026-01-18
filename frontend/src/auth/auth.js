const ADMIN_EMAIL = 'arvik3cr@gmail.com';

export const auth = {
  isAuthenticated: false,
  role: null,
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
    this.role = email === ADMIN_EMAIL ? 'admin' : 'user';
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
    localStorage.removeItem('API_KEY');
    localStorage.removeItem('USER_ROLE');
  },
};

auth.initialize();
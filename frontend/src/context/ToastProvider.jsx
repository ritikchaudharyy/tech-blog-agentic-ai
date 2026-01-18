import { createContext, useContext, useEffect, useState } from 'react';

const ToastContext = createContext(null);

export const useToast = () => useContext(ToastContext);

export const ToastProvider = ({ children }) => {
    const [toasts, setToasts] = useState([]);

    useEffect(() => {
        const handler = (e) => {
            const { type = 'info', message } = e.detail || {};
            if (!message) return;

            const id = Date.now();
            setToasts((prev) => [...prev, { id, type, message }]);

            setTimeout(() => {
                setToasts((prev) => prev.filter((t) => t.id !== id));
            }, 4000);
        };

        window.addEventListener('app:toast', handler);
        return () => window.removeEventListener('app:toast', handler);
    }, []);

    return (
        <ToastContext.Provider value={{}}>
            {children}

            {/* Toast Container */}
            <div className="fixed top-6 right-6 z-50 space-y-3">
                {toasts.map((toast) => (
                    <div
                        key={toast.id}
                        className={`px-4 py-3 rounded-lg shadow-lg text-sm font-medium animate-slide-in-right
              ${toast.type === 'error'
                                ? 'bg-red-600 text-white'
                                : toast.type === 'success'
                                    ? 'bg-green-600 text-white'
                                    : 'bg-slate-800 text-white'
                            }`}
                    >
                        {toast.message}
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    );
};

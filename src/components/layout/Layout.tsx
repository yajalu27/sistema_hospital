import React, { ReactNode, useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Users, 
  ClipboardList, 
  PlusCircle, 
  Menu, 
  X, 
  Receipt,
  Bell,
  User,
  Moon,
  Sun
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Initialize theme from localStorage or default to light
    return localStorage.getItem('theme') === 'dark' || 
           (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });
  const location = useLocation();

  // Update theme in localStorage and apply to document
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  const navItems = [
    { path: '/', icon: <Users size={20} />, label: 'Dashboard de Pacientes' },
    { path: '/discharges', icon: <ClipboardList size={20} />, label: 'Descargos de Pacientes' },
    { path: '/new-discharge', icon: <PlusCircle size={20} />, label: 'Generar Consumo' },
    { path: '/invoices', icon: <Receipt size={20} />, label: 'Facturas' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 flex flex-col">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 flex items-center">
              <svg className="w-8 h-8 mr-2 text-blue-500 dark:text-blue-300" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
              </svg>
              Sistema de Facturación Hospitalaria
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button 
              onClick={toggleTheme}
              className="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
            >
              {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <button className="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <Bell size={20} />
            </button>
            <button className="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <User size={20} />
            </button>
            <div className="md:hidden">
              <button 
                onClick={toggleMobileMenu}
                className="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100 p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar - Desktop */}
        <aside className="hidden md:flex md:w-64 flex-col bg-gradient-to-b from-blue-700 to-blue-900 dark:from-gray-900 dark:to-gray-800 text-white shadow-lg">
          <div className="p-4 border-b border-blue-600 dark:border-gray-700">
            <h2 className="text-lg font-semibold">Menú</h2>
          </div>
          <nav className="flex-1 mt-2 px-2 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`group flex items-center px-4 py-3 text-sm font-medium rounded-md transition-all duration-200 ${
                  location.pathname === item.path
                    ? 'bg-blue-600 dark:bg-gray-700 text-white shadow-inner'
                    : 'text-blue-100 dark:text-gray-300 hover:bg-blue-500 dark:hover:bg-gray-600 hover:text-white'
                }`}
              >
                <span className="mr-4">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>

        {/* Mobile menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden fixed inset-0 z-50 bg-black bg-opacity-50" onClick={toggleMobileMenu}>
            <div 
              className="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-300 ease-in-out"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-medium text-gray-900 dark:text-gray-100">Menú</h2>
                <button
                  onClick={toggleMobileMenu}
                  className="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100 focus:outline-none"
                >
                  <X size={24} />
                </button>
              </div>
              <nav className="mt-5 px-2 space-y-1">
                {navItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`group flex items-center px-4 py-3 text-sm font-medium rounded-md transition-all duration-200 ${
                      location.pathname === item.path
                        ? 'bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-300'
                        : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 hover:text-gray-900 dark:hover:text-gray-100'
                    }`}
                    onClick={toggleMobileMenu}
                  >
                    <span className="mr-4">{item.icon}</span>
                    {item.label}
                  </Link>
                ))}
              </nav>
            </div>
          </div>
        )}

        {/* Main content */}
        <main className="flex-1 p-6 lg:p-8">
          <div className="max-w-7xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
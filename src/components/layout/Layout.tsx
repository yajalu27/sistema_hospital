import React, { ReactNode, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Users, ClipboardList, PlusCircle, Menu, X, Receipt } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/', icon: <Users size={20} />, label: 'Dashboard de Pacientes' },
    { path: '/discharges', icon: <ClipboardList size={20} />, label: 'Descargos de Pacientes' },
    { path: '/new-discharge', icon: <PlusCircle size={20} />, label: 'Generar Consumo' },
    { path: '/invoices', icon: <Receipt size={20} />, label: 'Facturas' },
  ];

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-blue-600">Clínica Sistema</h1>
          </div>
          <div className="md:hidden">
            <button 
              onClick={toggleMobileMenu}
              className="text-gray-500 hover:text-gray-700 focus:outline-none"
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        {/* Sidebar - Desktop */}
        <aside className="hidden md:flex md:w-64 flex-col bg-white shadow-md">
          <nav className="mt-5 px-2 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`group flex items-center px-4 py-3 text-sm font-medium rounded-md ${
                  location.pathname === item.path
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <span className="mr-3">{item.icon}</span>
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>

        {/* Mobile menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden fixed inset-0 z-40 bg-black bg-opacity-25">
            <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg z-50">
              <div className="flex items-center justify-between h-16 px-4 border-b">
                <h2 className="text-lg font-medium text-blue-600">Menú</h2>
                <button
                  onClick={toggleMobileMenu}
                  className="text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  <X size={24} />
                </button>
              </div>
              <nav className="mt-5 px-2 space-y-1">
                {navItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`group flex items-center px-4 py-3 text-sm font-medium rounded-md ${
                      location.pathname === item.path
                        ? 'bg-blue-50 text-blue-600'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    onClick={toggleMobileMenu}
                  >
                    <span className="mr-3">{item.icon}</span>
                    {item.label}
                  </Link>
                ))}
              </nav>
            </div>
          </div>
        )}

        {/* Main content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
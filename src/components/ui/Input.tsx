// components/ui/Input.tsx
import React from 'react';

interface InputProps {
  label?: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  type?: string;
  placeholder?: string;
  icon?: React.ReactNode;
  className?: string;
  disabled?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      value,
      onChange,
      error,
      required = false,
      type = 'text',
      placeholder,
      icon,
      className = '',
      disabled = false,
    },
    ref
  ) => {
    return (
      <div className={`mb-4 ${className}`}>
        {label && (
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            {label}
            {required && <span className="text-red-500"> *</span>}
          </label>
        )}
        <div className="relative">
          {icon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {icon}
            </div>
          )}
          <input
            ref={ref}
            type={type}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            disabled={disabled}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              error
                ? 'border-red-500 dark:border-red-600'
                : 'border-gray-300 dark:border-gray-600'
            } ${icon ? 'pl-10' : ''} ${
              disabled
                ? 'bg-gray-100 dark:bg-gray-700 cursor-not-allowed'
                : 'bg-white dark:bg-gray-800'
            } dark:text-gray-100 transition-colors`}
            required={required}
          />
        </div>
        {error && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
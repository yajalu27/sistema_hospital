import React, { SelectHTMLAttributes } from 'react';

interface Option {
  value: string;
  label: string;
}

interface SelectProps extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'onChange'> {
  label?: string;
  options: Option[];
  error?: string;
  onChange: (value: string) => void;
}

const Select: React.FC<SelectProps> = ({
  label,
  options,
  error,
  className = '',
  onChange,
  value,
  ...props
}) => {
  return (
    <div className="mb-4">
      {label && (
        <label htmlFor={props.id} className="block text-sm font-medium text-gray-700 mb-1">
          {label}
        </label>
      )}
      <select
        className={`block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm
          ${error ? 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500' : 'border-gray-300'}
          ${className}`}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        {...props}
      >
        <option value="" disabled>
          Seleccionar...
        </option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Select;
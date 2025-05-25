import React, { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  title?: string;
  className?: string;
  headerActions?: ReactNode;
}

const Card: React.FC<CardProps> = ({ 
  children, 
  title, 
  className = '', 
  headerActions 
}) => {
  return (
    <div className={`bg-white rounded-lg shadow-sm overflow-hidden ${className}`}>
      {title && (
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>
          {headerActions && <div>{headerActions}</div>}
        </div>
      )}
      <div className="px-4 py-5 sm:p-6">{children}</div>
    </div>
  );
};

export default Card;
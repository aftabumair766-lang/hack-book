import React from 'react';
import { useAuth } from '../../components/Auth/AuthContext';
import styles from './AuthNavbarItem.module.css';

export default function AuthNavbarItem() {
  const { user, isAuthenticated, signout } = useAuth();

  const handleSignout = () => {
    signout();
    window.location.href = '/hack-book/';
  };

  if (isAuthenticated && user) {
    // Show user info and logout
    return (
      <div className={styles.authContainer}>
        <a href="/hack-book/dashboard" className={styles.authLink}>
          <span className={styles.userIcon}>👤</span>
          {user.full_name || user.email}
        </a>
        <button onClick={handleSignout} className={styles.logoutButton}>
          Logout
        </button>
      </div>
    );
  }

  // Show sign in and sign up links
  return (
    <div className={styles.authContainer}>
      <a href="/hack-book/signin" className={styles.authLink}>
        Sign In
      </a>
      <span className={styles.separator}>|</span>
      <a href="/hack-book/signup" className={styles.authLinkPrimary}>
        Sign Up
      </a>
    </div>
  );
}

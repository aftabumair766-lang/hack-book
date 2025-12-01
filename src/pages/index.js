import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <div className={styles.logoContainer}>
          <img
            src="/hack_book/img/book-cover.svg"
            alt="Physical AI & Humanoid Robotics"
            className={styles.bookCover}
          />
        </div>
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Learning 🚀
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  const features = [
    {
      title: '6 Comprehensive Chapters',
      description: (
        <>
          From foundations to future directions, covering anatomy, AI, control systems,
          locomotion, manipulation, and emerging challenges in humanoid robotics.
        </>
      ),
    },
    {
      title: 'Hands-On Exercises',
      description: (
        <>
          20+ practical exercises with code examples, simulations, and real-world
          applications to reinforce your learning.
        </>
      ),
    },
    {
      title: 'Industry Case Studies',
      description: (
        <>
          Learn from real robots: ASIMO, Atlas, Optimus, and more. Understand
          how theory translates to cutting-edge robotics systems.
        </>
      ),
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <div key={idx} className={clsx('col col--4')}>
              <div className="text--center padding-horiz--md">
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Comprehensive coursebook on Physical AI and Humanoid Robotics - Learn embodied intelligence, control systems, locomotion, and manipulation">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}

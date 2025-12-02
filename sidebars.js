/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main coursebook sidebar
  coursebookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: Foundations',
      items: [
        'chapter-01/chapter-01',
        'chapter-01/anatomy-structure',
        'chapter-01/sensors-actuators',
        'chapter-01/kinematics-dynamics',
        'chapter-01/exercises',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: AI in Physical Systems',
      items: ['chapter-02/chapter-02'],
    },
    {
      type: 'category',
      label: 'Chapter 3: Control Systems',
      items: ['chapter-03/chapter-03'],
    },
    {
      type: 'category',
      label: 'Chapter 4: Locomotion',
      items: ['chapter-04/chapter-04'],
    },
    {
      type: 'category',
      label: 'Chapter 5: Manipulation',
      items: ['chapter-05/chapter-05'],
    },
    {
      type: 'category',
      label: 'Chapter 6: Future Directions',
      items: ['chapter-06/chapter-06'],
    },
  ],
};

module.exports = sidebars;

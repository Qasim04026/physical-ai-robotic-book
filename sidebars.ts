import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
    tutorialSidebar: [
    'chapter_1_introduction_to_physical_ai',
    'chapter_2_embodied_intelligence',
    'chapter_3_ros2_fundamentals',
    'chapter_4_ros2_advanced',
    'chapter_5_robot_simulation_gazebo',
    'chapter_6_unity_for_robotics',
    'chapter_7_nvidi-isaac_platform',
    'chapter_8_Humanoid_Robot_Development',
    'chapter_9_Vision_Language_Action_Models',
    'chapter_10_Conversational_Robotics',
    'chapter_11_Sensor_Systems',
    'chapter_12_Capstone_Project',
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;

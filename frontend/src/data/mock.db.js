export const mockDB = {
  articles: [
    {
      id: 'a1',
      title: 'Agentic AI Systems: Architecture & Risks',
      summary:
        'Agentic AI systems extend LLMs with planning, memory, and tool use.',
      views: 18200,
      verified: true,
      status: 'Published',
      content: {
        sections: [
          {
            heading: 'What Are Agentic AI Systems?',
            text:
              'Agentic AI systems are designed to autonomously plan and act toward goals.',
          },
          {
            heading: 'Core Components',
            bullets: [
              'Planner',
              'Memory',
              'Tooling',
              'Executor',
            ],
          },
        ],
        sources: [
          'https://arxiv.org/abs/2308.00352',
          'https://openai.com/research',
        ],
      },
    },
    {
      id: 'a2',
      title: 'Retrieval-Augmented Generation (RAG)',
      summary:
        'RAG combines retrieval systems with generative models.',
      views: 14700,
      verified: true,
      status: 'Published',
    },
  ],

  analytics: {
    traffic7d: [
      { day: 'Mon', views: 4200 },
      { day: 'Tue', views: 4800 },
      { day: 'Wed', views: 5300 },
      { day: 'Thu', views: 6100 },
      { day: 'Fri', views: 7200 },
      { day: 'Sat', views: 6800 },
      { day: 'Sun', views: 7500 },
    ],
    metrics: {
      totalViews: 128430,
      articles: 342,
      revenue: 2840,
      readers: 9214,
    },
  },
};

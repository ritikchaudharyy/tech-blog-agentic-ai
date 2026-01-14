import { useEffect } from 'react';

const LanguageSelector = () => {
  useEffect(() => {
    // Prevent multiple injections
    if (document.getElementById('google-translate-script')) return;

    // Global init function (required by Google Translate)
    window.googleTranslateElementInit = () => {
      if (!window.google || !window.google.translate) return;

      new window.google.translate.TranslateElement(
        {
          pageLanguage: 'en',
          includedLanguages: 'en,hi,bn,te,mr,ta,ur,gu,kn,ml',
          autoDisplay: false,
          layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
        },
        'google_translate_element'
      );
    };

    // Inject Google Translate script
    const script = document.createElement('script');
    script.id = 'google-translate-script';
    script.src =
      'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    script.async = true;
    document.body.appendChild(script);

    // Cleanup is intentionally omitted:
    // Google Translate attaches global state and should persist across routes
  }, []);

  return (
    <div className="flex items-center">
      <div
        id="google_translate_element"
        className="glass px-2 py-1 text-sm"
        aria-label="Language selector"
      />
    </div>
  );
};

export default LanguageSelector;

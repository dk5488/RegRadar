/* ═══════════════════════════════════════════════════════════════════════
   RegRadar — useDebounce Hook
   Debounces a value by a specified delay, useful for search inputs.
   ═══════════════════════════════════════════════════════════════════════ */

import { useState, useEffect } from 'react';

export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Prefix internal links with the deploy base path (BASE_URL is '/' on
// GitHub Pages but '/<project>/' on plmlab GitLab Pages).
export function withBase(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, '');
  return `${base}/${path.replace(/^\/+/, '')}`;
}

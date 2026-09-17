import http from 'k6/http';
import { Counter } from 'k6/metrics';
import { check } from 'k6';

const uploadsOk = new Counter('uploads_ok');
const duplicates = new Counter('uploads_duplicated');

export const options = {
    stages: [
        { duration: '10s', target: 100 },
        { duration: '20s', target: 100 },
        { duration: '10s', target: 0 },
    ],
};

const BASE_URL = 'http://localhost:8000';

http.setResponseCallback(http.expectedStatuses(201, 409));

// Carga de PDFs en modo binario durante la inicialización (init context de k6)
const pdfFiles = [
    { name: '2020-Scrum-Guide-Spanish-Latin-South-American.pdf', data: open('./pdfs/2020-Scrum-Guide-Spanish-Latin-South-American.pdf', 'b') },
    { name: 'Essential-Kanban-Condensed-Spanish.pdf', data: open('./pdfs/Essential-Kanban-Condensed-Spanish.pdf', 'b') },
    { name: 'Filosofia Lean.pdf', data: open('./pdfs/Filosofia Lean.pdf', 'b') },
    { name: 'scrum_manager_historias_usuario.pdf', data: open('./pdfs/scrum_manager_historias_usuario.pdf', 'b') },
];

export default function () {
    const pdf = pdfFiles[Math.floor(Math.random() * pdfFiles.length)];

    const res = http.post(
        `${BASE_URL}/api/v1/documents/upload`,
        { file: http.file(pdf.data, pdf.name, 'application/pdf') },
    );

    const ok = res.status === 201;
    const dup = res.status === 409;
    if (ok) uploadsOk.add(1);
    if (dup) duplicates.add(1);

    check(res, {
        'upload procesado (201 o 409)': () => ok || dup,
    });
}
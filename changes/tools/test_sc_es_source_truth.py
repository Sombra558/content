import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

import sc_es_source_truth as sync  # noqa: E402


def text_slide(text, order_index=0):
    return {
        "order_index": order_index,
        "min_time": 3,
        "content_type": "Text",
        "content_type_unique_id": "text",
        "contents": [
            {
                "order_index": order_index,
                "text": {
                    "paragraphs": [text],
                    "instruction": "Read the following, then click Next.",
                },
            }
        ],
    }


def completion_slide(text, order_index=0):
    return {
        "order_index": order_index,
        "min_time": 3,
        "content_type": "Completion",
        "content_type_unique_id": "completion",
        "contents": [
            {
                "order_index": order_index,
                "text": {"instruction": "Click each item to learn more."},
                "interactive": {
                    "content_structure": [text],
                    "reveal_items": [
                        {"id": "item_1", "title": "PBW", "revealed_text": "61-4-120"}
                    ],
                },
            }
        ],
    }


def media_slide(order_index=0):
    return {
        "order_index": order_index,
        "min_time": 3,
        "content_type": "Media_sc_id_examples",
        "content_type_unique_id": "media_sc_id_examples",
        "preview_url": "images/sc-id-placeholder.png",
        "contents": [],
    }


class ReconcileUnitTests(unittest.TestCase):
    def test_reconcile_unit_uses_en_order_and_drops_es_only_orphans(self):
        en_slides = [
            text_slide("SC Code Sections 61-4-120 and 61-4-510 govern permits.", 0),
            text_slide("If you suspect drug interaction, slow or stop alcohol service.", 1),
            completion_slide("Permit types include {{item_1}}.", 2),
        ]
        es_slides = [
            text_slide("SC Code Sections 61-4-120 and 61-4-510 regulan permisos.", 0),
            media_slide(1),
            text_slide("Si sospecha interacción con drogas, reduzca o detenga el servicio de alcohol.", 2),
            completion_slide("Los permisos incluyen {{item_1}}.", 3),
        ]

        repaired, orphans, missing = sync.reconcile_unit(en_slides, es_slides, {})

        self.assertEqual(3, len(repaired))
        self.assertEqual([], missing)
        self.assertEqual([1], orphans)
        self.assertEqual(
            "SC Code Sections 61-4-120 and 61-4-510 regulan permisos.",
            repaired[0]["contents"][0]["text"]["paragraphs"][0],
        )
        self.assertEqual(
            "Si sospecha interacción con drogas, reduzca o detenga el servicio de alcohol.",
            repaired[1]["contents"][0]["text"]["paragraphs"][0],
        )
        self.assertEqual("completion", repaired[2]["content_type_unique_id"])

    def test_reconcile_unit_translates_missing_slide_with_override(self):
        en_slides = [
            text_slide("A simple way to verify age is to subtract 21 years from today's date.", 0),
        ]
        es_slides = []
        overrides = {
            "A simple way to verify age is to subtract 21 years from today's date.": {
                "paragraphs": [
                    "Una forma sencilla de verificar la edad es restar 21 años a la fecha de hoy."
                ]
            }
        }

        repaired, orphans, missing = sync.reconcile_unit(en_slides, es_slides, overrides)

        self.assertEqual([], orphans)
        self.assertEqual([], missing)
        self.assertEqual(
            "Una forma sencilla de verificar la edad es restar 21 años a la fecha de hoy.",
            repaired[0]["contents"][0]["text"]["paragraphs"][0],
        )

    def test_reconcile_unit_copies_missing_en_image_blocks(self):
        en_slides = [
            {
                "order_index": 0,
                "min_time": 3,
                "content_type": "Introduction",
                "content_type_unique_id": "introduction",
                "contents": [
                    {
                        "order_index": 0,
                        "content_type": "unit_introduction",
                        "text": {"bullet_points": ["2A. Topic"], "body": "Topics:"},
                    },
                    {
                        "order_index": 1,
                        "image": {
                            "placeholder": True,
                            "asset_id": "sc-img-standard-drink",
                            "alt": "Chart of standard drink equivalents.",
                            "status": "pending",
                        },
                    },
                ],
            }
        ]
        es_slides = [
            {
                "order_index": 0,
                "min_time": 3,
                "content_type": "Introduction",
                "content_type_unique_id": "introduction",
                "contents": [
                    {
                        "order_index": 0,
                        "content_type": "unit_introduction",
                        "text": {"bullet_points": ["2A. Tema"], "body": "Temas:"},
                    }
                ],
            }
        ]

        repaired, _, missing = sync.reconcile_unit(en_slides, es_slides, {})

        self.assertEqual([], missing)
        image_assets = [
            content["image"]["asset_id"]
            for content in repaired[0]["contents"]
            if "image" in content
        ]
        self.assertEqual(["sc-img-standard-drink"], image_assets)


class KeywordMapTests(unittest.TestCase):
    def test_build_es_keyword_map_includes_spanish_audit_phrases(self):
        rubric_es = sync.build_es_keyword_map(sync.EN_AUDIT_KEYWORDS)

        self.assertIn("recent SC enforcement stats", rubric_es)
        self.assertIn("scdps", rubric_es["recent SC enforcement stats"])
        self.assertIn(
            "capacitación de repaso",
            rubric_es["ongoing training / refreshers"],
        )
        self.assertIn(
            "consentimiento implícito",
            rubric_es["implied consent"],
        )


if __name__ == "__main__":
    unittest.main()

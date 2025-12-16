import unittest

from secure.headers import CrossOriginEmbedderPolicy
from secure.headers.base_header import HeaderDefaultValue


class TestCrossOriginEmbedderPolicy(unittest.TestCase):
    def test_default_value(self) -> None:
        """Default COEP should be `require-corp`."""
        policy = CrossOriginEmbedderPolicy()
        self.assertEqual(policy.header_value, HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value)

    def test_builder_helpers(self) -> None:
        """Helper methods should set predictable directives."""
        self.assertEqual(CrossOriginEmbedderPolicy().require_corp().header_value, "require-corp")
        self.assertEqual(CrossOriginEmbedderPolicy().credentialless().header_value, "credentialless")
        self.assertEqual(CrossOriginEmbedderPolicy().unsafe_none().header_value, "unsafe-none")

    def test_value_accepts_custom(self) -> None:
        """`value()` should normalize and accept arbitrary strings."""
        policy = CrossOriginEmbedderPolicy().value("CUSTOM-Policy ")
        self.assertEqual(policy.header_value, "custom-policy")

    def test_invalid_inputs_raise(self) -> None:
        """CR/LF should be rejected when setting a value."""
        with self.assertRaises(ValueError):
            CrossOriginEmbedderPolicy().value("bad\rvalue")

    def test_deterministic_output(self) -> None:
        """Calling helpers repeatedly should yield the same header text."""
        first = CrossOriginEmbedderPolicy().credentialless()
        second = CrossOriginEmbedderPolicy().credentialless().credentialless()
        self.assertEqual(first.header_value, second.header_value)


if __name__ == "__main__":
    unittest.main()

"""Regression for encoded DTD declarations and manifest extraction."""
from defusedxml.common import DefusedXmlException
import pytest
from graphify.extract import extract_lazarus_package
from graphify.manifest_ingest import _parse_pom

def test_utf16_dtd_is_rejected(tmp_path):
    path = tmp_path / "hostile.lpk"
    path.write_bytes('<?xml version="1.0" encoding="UTF-16"?><!DOCTYPE CONFIG [<!ENTITY demo "unexpected">]><CONFIG><Package><Name Value="&demo;"/></Package></CONFIG>'.encode("utf-16"))
    result = extract_lazarus_package(path)
    assert not result["nodes"]
    assert result.get("error")

def test_maven_forbids_dtd_and_allows_normal_manifest():
    with pytest.raises(DefusedXmlException):
        _parse_pom('<!DOCTYPE project [<!ENTITY demo "unexpected">]><project><artifactId>&demo;</artifactId></project>')
    assert _parse_pom("<project><artifactId>normal</artifactId></project>")["name"] == "normal"

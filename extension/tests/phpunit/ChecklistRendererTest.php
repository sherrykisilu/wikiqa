<?php

declare( strict_types=1 );

namespace MediaWiki\Extension\WikiQA\Tests;

use MediaWiki\Extension\WikiQA\ChecklistRenderer;
use MediaWiki\Extension\WikiQA\Hooks;
use MediaWiki\Parser\Parser;
use PHPUnit\Framework\TestCase;

class ChecklistRendererTest extends TestCase {
	public function testRenderEscapesTitleAndNormalisesStatus(): void {
		$parser = new Parser();
		$result = ChecklistRenderer::render( $parser, '<Release>', 'READY' );

		$this->assertTrue( $result['isHTML'] );
		$this->assertStringContainsString( '&lt;Release&gt;', $result[0] );
		$this->assertStringContainsString( 'data-status="ready"', $result[0] );
		$this->assertSame( [ 'ext.wikiQA.styles' ], $parser->getOutput()->modules );
	}

	public function testUnknownStatusFallsBackToDraft(): void {
		$this->assertSame( 'draft', ChecklistRenderer::normaliseStatus( 'unknown' ) );
	}

	public function testParserHookIsRegistered(): void {
		$parser = new Parser();
		Hooks::onParserFirstCallInit( $parser );

		$this->assertArrayHasKey( 'qaChecklist', $parser->hooks );
	}
}

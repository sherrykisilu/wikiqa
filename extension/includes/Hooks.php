<?php

declare( strict_types=1 );

namespace MediaWiki\Extension\WikiQA;

use MediaWiki\Parser\Parser;

class Hooks {
	public static function onParserFirstCallInit( Parser $parser ): void {
		$parser->setFunctionHook( 'qaChecklist', [ ChecklistRenderer::class, 'render' ] );
	}
}
